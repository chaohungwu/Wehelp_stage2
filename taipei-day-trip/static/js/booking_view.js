// 訂單預定畫面渲染
async function build_booking_view(get_booking_data){
    
    username = localStorage.getItem('user_name')

    console.log(get_booking_data["data"]["data"])
    document.querySelector("#welcome_title").textContent=`您好，${username}，待預定的行程如下：`

    if (get_booking_data["data"]["data"]==null){
        // 1. 沒預定狀態
        text_dom = document.createElement("div")
        text_dom.className="no_booking_title"
        text_dom.textContent = "目前沒有任何待預定的行程"
        document.querySelector(".booking_contain").appendChild(text_dom)
        document.querySelector(".booking_contain").style.height="auto"


    }else{
        //2. 有預訂狀態 
        // 將隱藏的內容做顯示
        let booking_view1_dom = document.querySelector(".booking_contain_attraction_content")
        booking_view1_dom.style.display='flex'

        booking_view1_dom = document.querySelector(".hr_style")
        booking_view1_dom.style.display='flex'
        booking_view1_dom = document.querySelector(".hr_style")
        booking_view1_dom.style.display='flex'
        booking_view1_dom = document.querySelector(".hr_style")
        booking_view1_dom.style.display='flex'

        booking_view1_dom = document.querySelector(".booking_contain_contact")
        booking_view1_dom.style.display='flex'

        booking_view1_dom = document.querySelector(".booking_contain_CreditCard")
        booking_view1_dom.style.display='flex'

        booking_view1_dom = document.querySelector(".sum_booking_info_contain")
        booking_view1_dom.style.display='flex'

        booking_footer_dom = document.querySelector(".footer_HomePage")

        booking_footer_dom.style.height="50px"
        booking_footer_dom.style.position="relative"
        booking_footer_dom.style.alignItems="center"
        booking_footer_dom.style.paddingTop="0px"


        // 將內容填入，這邊收訊息帶入
        console.log(get_booking_data)

        let att_data_dom = document.querySelector("#booking_att_name")
        att_data_dom.textContent = `台北一日遊：${get_booking_data['data']["data"]['attraction']['name']}`;

        att_data_dom = document.querySelector("#booking_date")
        att_data_dom.textContent = get_booking_data['data']["data"]['date'];


        att_data_dom = document.querySelector("#booking_time")
        if(get_booking_data['data']["data"]['time']=='morning'){
            att_data_dom.textContent = "早上9點到下午4點"
        }else{
            att_data_dom.textContent = "下午2點到晚上9點"
        }
        att_data_dom = document.querySelector("#booking_price")
        att_data_dom.textContent = `新台幣 ${get_booking_data['data']["data"]['price']} 元`;

        att_data_dom = document.querySelector("#booking_address")
        att_data_dom.textContent = get_booking_data['data']["data"]['attraction']['address'];
        
        att_data_dom = document.querySelector(".booking_contain_attraction_content__img")
        att_data_dom.style.backgroundImage = `url(${get_booking_data['data']["data"]['attraction']['image']})`;

        att_data_dom = document.querySelector(".sum_booking_info_contain_Title")
        att_data_dom.textContent = `總價：新台幣 ${get_booking_data['data']["data"]['price']} 元`;

    }
}
