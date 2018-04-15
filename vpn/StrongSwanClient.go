package main

import (
	"fmt"
	"github.com/bronze1man/goStrongswanVici"
)

func main() {
	fmt.Println("Init success")

	client, err := goStrongswanVici.NewClientConnFromDefaultSocket()

	if err != nil {
		panic(err)
	}

	// deallocate the resource
	defer client.Close()


	childConfigMap := make(map[string]goStrongswanVici.ChildSAConf)
	childSAConfig := goStrongswanVici.ChildSAConf{
		Local_ts:      []string{"10.0.1.0/24"},
		Remote_ts:     []string{"10.0.2.0/24"},
		ESPProposals:  []string{"aes256-sha256-modp2048"},
		StartAction:   "trap",
		CloseAction:   "restart",
		Mode:          "tunnel",
		ReqID:         "10",
		RekeyTime:     "10m",
		InstallPolicy: "no",
	}
	childConfigMap["test-child-conn"] = childSAConfig

	localAuthConf := goStrongswanVici.AuthConf{
		AuthMethod: "psk",
	}
	remoteAuthConf := goStrongswanVici.AuthConf{
		AuthMethod: "psk",
	}

	ikeConfMap := make(map[string] goStrongswanVici.IKEConf)

	ikeConf := goStrongswanVici.IKEConf{
		LocalAddrs:  []string{"192.168.56.102"},
		RemoteAddrs: []string{"192.168.56.103"},
		Proposals:   []string{"aes256-sha256-modp2048"},
		Version:     "1",
		LocalAuth:   localAuthConf,
		RemoteAuth:  remoteAuthConf,
		Children:    childConfigMap,
		Encap:       "no",
	}

	ikeConfMap["test-connection"] = ikeConf

	//load connenction information into strongswan
	err = client.LoadConn(&ikeConfMap)
	if err != nil {
		fmt.Printf("error loading connection: %v")
		panic(err)
	}

	sharedKey := &goStrongswanVici.Key{
		Typ:    "IKE",
		Data:   "this is the key",
		Owners: []string{"192.168.198.10"}, //IP of the remote host
	}

	//load shared key into strongswan
	err = client.LoadShared(sharedKey)
	if err != nil {
		fmt.Printf("error returned from loadsharedkey \n")
		panic(err)
	}

	//list-conns
	connList, err := client.ListConns("")
	if err != nil {
		fmt.Printf("error list-conns: %v \n", err)
	}

	for _, connection := range connList {
		fmt.Printf("connection map: %v", connection)
	}

	// get all conns info from strongswan
	connInfo, err := client.ListAllVpnConnInfo()
	if err != nil {
		panic(err)
	}
	fmt.Printf("found %d connections. \n", len(connInfo))

	//unload connection from strongswan
	unloadConnReq := &goStrongswanVici.UnloadConnRequest{
		Name: "test-connection",
	}
	err = client.UnloadConn(unloadConnReq)
	if err != nil {
		panic(err)
	}

	// kill all conns in strongswan
	for _, info := range connInfo {
		fmt.Printf("kill connection id %s\n", info.Uniqueid)
		err = client.Terminate(&goStrongswanVici.TerminateRequest{
			Ike_id: info.Uniqueid,
		})
		if err != nil {
			panic(err)
		}
	}


	v, err := client.Version()
	if err != nil {
		panic(err)
	}

	fmt.Println("StrongSwan version : %#v", v)
}
