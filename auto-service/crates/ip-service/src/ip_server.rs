use common::services::{self, CommonClient, Services};
use service_protos::proto_ip_service::{
    ip_server::Ip, AddRequest, AddResponse, ListRequest, ListResponse, NetDevice,
};
use tokio::{io::AsyncWriteExt, sync::Mutex};
use tonic::{Request, Response, Result, Status};

use std::{collections::HashMap, io::ErrorKind, net::ToSocketAddrs, path::Path};

const REMOTE_IP_DIR: &str = "/share/samba/tmp";

#[derive(Default, Debug)]
pub struct IpServer {
    pub conn_clients: Mutex<CommonClient>,
    pub remotes: Mutex<HashMap<String, Vec<NetDevice>>>,
}

impl IpServer {
    async fn sync_remote_ip_to_disk(&self, client_ip: String) {
        let remote_ip_dir = Path::new(REMOTE_IP_DIR);
        match tokio::fs::create_dir(remote_ip_dir).await {
            Ok(_) => {}
            Err(e) => {
                if e.kind() != ErrorKind::AlreadyExists {
                    panic!("create dir error")
                }
            }
        }
        let file_path = remote_ip_dir.join(client_ip.clone());
        let mut f = tokio::fs::OpenOptions::new()
            .write(true)
            .create(true)
            .truncate(true)
            .open(file_path)
            .await
            .expect("open remote_ip_file error");
        let remote = self.remotes.lock().await;
        if let Some(remote_ip) = remote.get(&client_ip) {
            if let Ok(src) = serde_json::to_string(remote_ip) {
                f.write_all(src.as_bytes()).await.unwrap();
            }
        }
    }
}

#[async_trait::async_trait]
impl services::Services for IpServer {
    async fn set_client_info<T>(&self, request: Request<T>)
    where
        T: Send,
    {
        if let Some(addr) = request.remote_addr() {
            self.conn_clients
                .lock()
                .await
                .set_client(addr.ip().to_string(), String::new());
            if let Ok(hostname) = addr
                .to_socket_addrs()
                .and_then(|mut addrs| addrs.next().ok_or(ErrorKind::AddrNotAvailable.into()))
            {
                self.conn_clients
                    .lock()
                    .await
                    .set_client(addr.ip().to_string(), hostname.to_string());
            }
        }
    }

    async fn get_client_info<T>(&self, request: &Request<T>) -> (String, String)
    where
        T: Send + std::marker::Sync,
    {
        if let Some(addr) = request.remote_addr() {
            self.conn_clients
                .lock()
                .await
                .set_client(addr.ip().to_string(), String::new());
            if let Ok(hostname) = addr
                .to_socket_addrs()
                .and_then(|mut addrs| addrs.next().ok_or(ErrorKind::AddrNotAvailable.into()))
            {
                (addr.ip().to_string(), hostname.to_string())
            } else {
                (addr.ip().to_string(), String::new())
            }
        } else {
            (String::new(), String::new())
        }
    }
}

#[async_trait::async_trait]
impl Ip for IpServer {
    async fn list(&self, request: Request<ListRequest>) -> Result<Response<ListResponse>, Status> {
        println!("list request = {:?}", request);
        self.set_client_info(request).await;
        let response = Response::new(ListResponse::default());
        println!("IpServer.conn_client = {:?}", self.conn_clients);
        println!("list response = {:?}", response);
        Ok(response)
    }

    async fn add_remote(
        &self,
        mut request: Request<AddRequest>,
    ) -> Result<Response<AddResponse>, Status> {
        println!("add_remote request = {:?}", request);
        let remote_net_devices = request.get_mut().clone().net_devices;
        let (client_ip, _) = self.get_client_info(&request).await;
        self.remotes
            .lock()
            .await
            .insert(client_ip.clone(), remote_net_devices);
        self.set_client_info(request).await;
        self.sync_remote_ip_to_disk(client_ip).await;
        let response = Response::new(AddResponse::default());
        println!("IpServer = {:?}", self);
        println!("add_remote response = {:?}", response);
        Ok(response)
    }
}
