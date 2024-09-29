use service_protos::proto_ip_service;
use tokio;
use tonic::transport::Server;

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
    create_service().await;
    println!("Hello, world!");
}

pub async fn create_service() {
    let addr = "[::1]:50001".parse().expect("cannot parse addr");
    let server = ip_service::ip::IpServer::default();
    let svc = proto_ip_service::ip_server::IpServer::new(server);
    Server::builder()
        .add_service(svc)
        .serve(addr)
        .await
        .expect("serve server err!");
}
