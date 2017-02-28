package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
)

type Menu struct {
	Button []Button `json:"button"`
}

type ClickButton struct {
	Typename string `json:"type"`
	Name     string `json:"name"`
	Key      string `json:"key"`
}

type ViewButton struct {
	Typename string `json:"type"`
	Name     string `json:"name"`
	Url      string `json:"url"`
}

type SubButton struct {
	Name   string   `json:"name"`
	SubBtn []Button `json:"sub_button"`
}

type Button interface {
}

func NewClickButton(name string, key string) *ClickButton {
	return &ClickButton{"click", name, key}
}

func NewViewButton(name string, url string) *ViewButton {
	return &ViewButton{"view", name, url}
}

var (
	base_uri     = `https://api.weixin.qq.com/cgi-bin`
	access_token = os.Getenv("ACCESS_TOKEN")
)

func main() {
	btns := []Button{
		NewViewButton(
			"进店选米",
			"http://www.baidu.com",
		),
		NewViewButton(
			"产品价格单",
			"http://ladrift.cn/priceList.html",
		),
		SubButton{
			"联系我们",
			[]Button{
				NewViewButton(
					"大宗预定",
					"http://ladrift.cn/book.html",
				),
				NewClickButton(
					"大客户专线",
					"business_line_number",
				),
				NewClickButton(
					"来米客服",
					"laimi_service_number",
				),
			},
		},
	}

	menu := Menu{btns}

	b, err := json.Marshal(menu)
	if err != nil {
		fmt.Fprint(os.Stderr, err)
		os.Exit(-1)
	}
	fmt.Println(string(b))

	buf := bytes.NewBuffer(b)
	uri := base_uri + `/menu/create?access_token=` + access_token

	fmt.Println(uri)
	resp, err := http.Post(uri, `application/json`, buf)
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
