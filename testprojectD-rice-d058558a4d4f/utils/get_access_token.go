package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
)

func main() {
	u, err := url.Parse(`https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET`)
	if err != nil {
		fmt.Fprint(os.Stderr, err)
		os.Exit(-1)
	}
	q := u.Query()
	q.Set(`appid`, `wxd5be3f594df0e2e3`)
	q.Set(`secret`, `8bc9ae0fd136bcc10837a094c563a834`)
	u.RawQuery = q.Encode()
	fmt.Println(u.String())
	resp, err := http.Get(u.String())
	if err != nil {
		fmt.Fprint(os.Stderr, err)
		os.Exit(-1)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Fprint(os.Stderr, err)
		os.Exit(-1)
	}
	fmt.Println(string(body))
}
