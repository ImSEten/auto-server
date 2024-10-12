use clap::{CommandFactory, Parser};
use tonic::transport::Server;

mod flags;

use service_protos::proto_ip_service;

pub struct AutoServer {
    ip: String,
    port: u16,
}

impl AutoServer {
    pub fn new(ip: String, port: u16) -> Self {
        AutoServer { ip, port }
    }
}

fn main() {
    let runtime = tokio::runtime::Builder::new_multi_thread()
        .enable_all()
        .worker_threads(2)
        .max_blocking_threads(2)
        .build()
        .expect("build tokio runtime error!");
    runtime.block_on(async_main());
}

async fn async_main() {
    // TODO: let flags = flags.parse(); // flags is Options
    let parse_flags = flags::Flags::parse();
    match parse_flags.command {
        Some(flags::Commands::Start { ip, port }) => {
            let auto_server = AutoServer::new(ip, port);
            println!("service starting...");
            create_service(auto_server).await;
            println!("service exited");
        }
        Some(flags::Commands::Stop) => {
            println!("not implement!")
        }
        None => {
            if let Err(e) = flags::Flags::command().print_help() {
                println!("print_help failed {:?}", e);
            };
        }
    }
}

pub async fn create_service(auto_server: AutoServer) {
    let addr = (auto_server.ip.clone() + ":" + auto_server.port.to_string().as_str())
        .parse()
        .expect("cannot parse addr");
    println!(
        "Server is listening to {}:{}",
        auto_server.ip, auto_server.port
    );
    let server = ip_service::ip_server::IpServer::default();
    let svc = proto_ip_service::ip_server::IpServer::new(server);
    Server::builder()
        .add_service(svc)
        .serve(addr)
        .await
        .expect("serve server err!");
}
