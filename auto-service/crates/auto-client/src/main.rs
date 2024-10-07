use std::sync::Arc;
use tokio::sync::Mutex;

const IP: &str = "192.168.99.3";
const PORT: &str = "10086";

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
    let client = ip_service::ip_client::Client::new(IP.to_string(), PORT.to_string()).await;
    let client = Arc::new(Mutex::new(client));
    let handle = ip_service::ip_client::monitor_ip::<String>(client.clone()).await;
    let _ = tokio::join!(handle);
}
