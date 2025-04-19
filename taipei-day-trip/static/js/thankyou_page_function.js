let url = location.href;

order_num = url.slice(url.lastIndexOf("=")+1)
console.log(order_num)


async function order_info_get() {
    let response = await fetch(`/api/order/${order_num}`,
        {
            method:'GET',
            headers: {
            "Authorization": `Bearer ${localStorage.getItem('token')}`
            }
        })

    let data = await response.json();
    console.log(data)

    try {
        let order_num_text = document.querySelector(".thank_text")
        order_num_text.textContent=`您的訂單編號為 ${order_num}，感謝您的預定，若有相關疑問，歡迎透過email來信詢問~!`
        
        // 圖片
        order_img = document.querySelector("#order_img")
        // console.log(data["data"]["data"]['trip']["attraction"]["image"])
        order_img.style.backgroundImage=`url('${data["data"]["data"]['trip']["attraction"]["image"]}')`
        
        // 名稱
        order_att_name = document.querySelector("#order_name")
        order_att_name.textContent=`${data["data"]["data"]['trip']["attraction"]['name']}`
    
    
        // 日期
        order_date = document.querySelector("#order_date")
        order_date.textContent=`${data["data"]["data"]['trip']["date"]}`
        
        // 時間
        order_time = document.querySelector("#order_time")
        order_time.textContent=`${data["data"]["data"]['trip']["time"]}`
        
        // 地點
        order_address = document.querySelector("#order_address")
        order_address.textContent=`${data["data"]["data"]['trip']["attraction"]['address']}`
    

      } catch (error) {
        window.location.href = "/";
      }

}
// order_info_get()
window.onload =  order_info_get()


