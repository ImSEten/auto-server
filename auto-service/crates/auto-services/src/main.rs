use service_protos::proto_ip_service;
use tonic::transport::Server;

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
    println!("service creating...");
    create_service().await;
    println!("service exited");
}

pub async fn create_service() {
    // ip_service::ip_common::get_net_info().await;

    let addr = (IP.to_string() + ":" + PORT)
        .parse()
        .expect("cannot parse addr");
    // let addr = "192.168.99.3:10086".parse().expect("cannot parse addr");
    // let addr = "[::]:10086".parse().expect("cannot parse addr");
    let server = ip_service::ip_server::IpServer::default();
    let svc = proto_ip_service::ip_server::IpServer::new(server);
    Server::builder()
        .add_service(svc)
        .serve(addr)
        .await
        .expect("serve server err!");
}
