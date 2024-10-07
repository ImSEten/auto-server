use std::sync::Arc;

use service_protos::proto_ip_service::{ip_client::IpClient, AddRequest, ListRequest, NetDevice};
use tokio::{sync::Mutex, task::JoinHandle};
use tonic::{transport::Channel, Status};

use crate::ip_common::get_net_info;

#[derive(Default, Debug, Clone)]
pub struct Client {
    pub server_ip: String,
    pub port: String,
    pub client: Option<IpClient<Channel>>,
    net_devices: Vec<NetDevice>,
}

pub struct IpService {
    pub net_devices: Arc<Vec<NetDevice>>,
}

impl Client {
    pub async fn new(server_ip: String, port: String) -> Self {
        Client {
            server_ip: server_ip.clone(),
            port: port.clone(),
            client: IpClient::connect(
                "http://".to_string() + server_ip.as_str() + ":" + port.as_str(),
            )
            .await
            .ok(),
            net_devices: Vec::<NetDevice>::new(),
        }
    }

    pub async fn list(&mut self) {
        println!("list request to server");
        if let Some(client) = self.client.as_mut() {
            let response = client
                .list(ListRequest::default())
                .await
                .expect("list request error");
            println!("response = {:?}", response);
        };
    }

    pub async fn add_remote(&mut self) -> Result<(), Status> {
        let request = AddRequest {
            net_devices: self.net_devices.clone(),
        };
        if let Some(client) = self.client.as_mut() {
            match client.add_remote(request).await {
                Ok(_) => Ok(()),
                Err(e) => {
                    self.re_connect().await;
                    Err(e)
                }
            }
        } else {
            self.re_connect().await;
            Err(Status::invalid_argument("client is None"))
        }
    }

    pub async fn re_connect(&mut self) {
        self.client = IpClient::connect(
            "http://".to_string() + self.server_ip.as_str() + ":" + self.port.as_str(),
        )
        .await
        .ok();
    }
}

pub async fn monitor_ip<T>(client: Arc<Mutex<Client>>) -> JoinHandle<T>
where
    T: std::marker::Send + 'static,
{
    tokio::spawn(async move {
        loop {
            let net_devices = get_net_info().await;
            let mut c = client.lock().await;
            if c.net_devices != net_devices {
                let pre_net_devices = c.net_devices.clone();
                c.net_devices = net_devices;
                match c.add_remote().await {
                    Ok(_) => {}
                    Err(e) => {
                        println!("add_remote error: {:?}", e);
                        c.net_devices = pre_net_devices;
                    }
                }
            }
            tokio::time::sleep(tokio::time::Duration::from_secs(10)).await;
        }
    })
}
