use clap::{CommandFactory, Parser};
use std::sync::Arc;
use tokio::sync::Mutex;

use ip_service::{ip_client::Client, ip_common::get_net_info};

mod flags;

fn main() {
    let runtime = tokio::runtime::Builder::new_multi_thread()
        .enable_all()
        .worker_threads(2)
        .max_blocking_threads(2)
        .build()
        .expect("build tokio runtime error!");
    runtime.block_on(async_main());
}

async fn create_client(server_ip: String, port: String) -> Arc<Mutex<Client>> {
    Arc::new(Mutex::new(
        Client::new(server_ip.to_string(), port.to_string()).await,
    ))
}

async fn async_main() {
    let parse_flags = flags::Flags::parse();
    let client = create_client(flags::IP.to_string(), flags::PORT.to_string()).await;
    match parse_flags.command {
        Some(flags::Commands::IpService { command }) => match command {
            Some(flags::IpServiceCommand::AddRemote {}) => {
                if let Err(e) = client
                    .lock()
                    .await
                    .add_remote(get_net_info().await.expect("get net info error"))
                    .await
                {
                    println!("add remote returns error: {:?}", e);
                }
            }
            Some(flags::IpServiceCommand::List {}) => match client.lock().await.list().await {
                Ok(response) => {
                    println!("list result = {:?}", response);
                }
                Err(e) => {
                    println!("list returns error: {:?}", e);
                    panic!("list error!");
                }
            },
            Some(flags::IpServiceCommand::MonitorIp {}) => {
                let client = create_client(flags::IP.to_string(), flags::PORT.to_string()).await;
                let handle = ip_service::ip_common::monitor_ip(client.clone()).await;
                let _ = tokio::join!(handle);
            }
            None => {
                let mut cmd = flags::Flags::command();
                for s in cmd.get_subcommands_mut() {
                    if s.get_name() == "ip_service" {
                        s.print_help().expect("print ip_service help failed");
                    }
                }
            }
        },
        None => {
            if let Err(e) = flags::Flags::command().print_help() {
                println!("print_help failed {:?}", e);
            };
        }
    }
}
