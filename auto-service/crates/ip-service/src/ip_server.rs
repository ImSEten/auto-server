use common::services::{self, CommonClient, Services};
use service_protos::proto_ip_service::{
    ip_server::Ip, AddRequest, AddResponse, ListRequest, ListResponse, NetDevice,
};
use tokio::sync::Mutex;
use tonic::{Request, Response, Result, Status};

use std::{collections::HashMap, io::ErrorKind, net::ToSocketAddrs};

#[derive(Default, Debug)]
pub struct IpServer {
    pub conn_clients: Mutex<CommonClient>,
    pub remotes: Mutex<HashMap<String, Vec<NetDevice>>>,
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
            .insert(client_ip, remote_net_devices);
        self.set_client_info(request).await;
        let response = Response::new(AddResponse::default());
        println!("IpServer = {:?}", self);
        println!("add_remote response = {:?}", response);
        Ok(response)
    }
}
