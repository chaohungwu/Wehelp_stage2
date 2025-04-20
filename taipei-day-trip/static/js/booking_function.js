// 1. 送訂單到後端
// 這邊在建立訂單時會將尚未建立的訂單資訊存在session storage
async function build_booking(){

    let response1 = await fetch(`/api/auth`,
        {
            method:'GET',
            headers: {
            "Authorization": `Bearer ${localStorage.getItem('token')}`
            }
        })
    let data1 = await response1.json();
    let user_info = data1['data']
    let aaa = await signin_license_check()

    // 如果使用者沒有登入，有自動打開登入畫面，就自動打開
    if(user_info==null){
        signin_enter()

    }else{
        
        let att_id_select = att_id
        let date_select = document.querySelector(".date_style").value
        let time = document.querySelectorAll('.radio-input');

        for(var i = 0; i < time.length; i++){
        if(time[i].checked){
            time_id = time[i].id; //選取時間的值
            }
        }

        let response = await fetch("/api/booking",// 要連結的連結
            {
                method:"POST",
                headers:{"Authorization": `Bearer ${localStorage.getItem('token')}`},

                //發送請求到後方並戴上這些json
                body:JSON.stringify({
                                    "att_id_select":att_id_select,
                                    "date_select":date_select,
                                    "time_id":time_id,
                                    })
            });

        let data =await response.json();
        console.log(data)
        window.location.href = `/booking`
    }

}

// 2. 取得使用者預定資訊
async function get_booking_info(){
    let response = await fetch("/api/booking", {
        method: 'GET',
        headers: {
            "Authorization": `Bearer ${localStorage.getItem('token')}`
        }
    });
    
    let data = await response.json();
    // console.log(`訂單資訊：${data}`)
    return data;
    }

    
// 3. 刪除預訂資料
async function delete_booking(){
    let response = await fetch("/api/booking", {
        method: 'DELETE',
        headers: {
            "Authorization": `Bearer ${localStorage.getItem('token')}`
        }
    });

    let data = await response.json();
    console.log(data)

    // 刪除後重新整理頁面
    window.location.reload();
}


// 3. 預定畫面按鈕功能(進入booking頁面)
async function booking_page(){
    let response = await fetch(`/api/auth`,
        {
            method:'GET',
            headers: {
            "Authorization": `Bearer ${localStorage.getItem('token')}`
            }
        })
        let data = await response.json();
        let user_info = data['data']
        let aaa = await signin_license_check()
        console.log(user_info)
        // console.log(aaa)

        // 如果使用者沒有登入，有自動打開登入畫面，就自動打開
        if(user_info==null){
            // sessionStorage.setItem("singin_enter_autoopen", "true");
            // window.location.href = "/";
            signin_enter()

        // 如果有登入的話就跳到預定頁面(/booking)
        }else{
            window.location.href = `/booking`
        }
    }






