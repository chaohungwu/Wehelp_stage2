

async function userInfoView(){
    let response = await fetch(`/api/auth`,
        {
          method:'GET',
          headers: {
          "Authorization": `Bearer ${localStorage.getItem('token')}`
          }
        })

    let user_data = await response.json();

    console.log(user_data['data'])
    let new_dom = document.createElement("div");
    new_dom.textContent=user_data['data']['name']
    document.querySelector("#user_name").appendChild(new_dom)

    let new_mail_dom = document.createElement("div")
    new_mail_dom.textContent=user_data['data']['email']
    document.querySelector("#user_mail").appendChild(new_mail_dom)

    let user_img_dom = document.querySelector(".user_img");
    user_img_dom.style.backgroundImage=`url("${user_data['data']['img']}")`


}
userInfoView()





async function getOrderInfo(){
    let response = await fetch(`/api/order_history`,
        {
          method:'GET',
          headers: {
          "Authorization": `Bearer ${localStorage.getItem('token')}`
          }
        })

    let order_history = await response.json();
    console.log(order_history)
    // console.log(order_history.length)
    console.log(order_history['data'])


    for(let i=0 ; i<order_history['data'].length; i++){

        new_order_card = document.createElement("div")
        new_order_card.className = "order_card"
        new_order_card.id = `order_card_${i}`
        document.querySelector(".user_order_content").appendChild(new_order_card)

        new_order_card.addEventListener('click', () => {
            window.location.href = `/thankyou?number=${order_history['data'][i][10]}`
        })


        new_order_info_contain = document.createElement("div")
        new_order_info_contain.className = "order_info_contain"
        new_order_info_contain.id = `order_info_contain_${i}`
        document.querySelector(`#order_card_${i}`).appendChild(new_order_info_contain)

        order_info_group = document.createElement("div")
        order_info_group.className = `order_info_group`
        order_info_group.id = `order_info_group_${i}`

        document.querySelector(`#order_info_contain_${i}`).appendChild(order_info_group)



        new_order_info_title1 = document.createElement("div")
        new_order_info_title1.className = "order_info_title"
        new_order_info_title1.textContent= `預約活動日期：${order_history['data'][i][3]}`
        document.querySelector(`#order_info_group_${i}`).appendChild(new_order_info_title1)


        new_order_info_title2 = document.createElement("div")
        new_order_info_title2.className = "order_info_title"
        new_order_info_title2.textContent= `訂單編號：${order_history['data'][i][10]}`
        document.querySelector(`#order_info_group_${i}`).appendChild(new_order_info_title2)



        new_order_card_img = document.createElement("div")
        new_order_card_img.className = "order_img"



        let response = await fetch(`/api/order/${order_history['data'][i][10]}`,
            {
                method:'GET',
                headers: {
                "Authorization": `Bearer ${localStorage.getItem('token')}`
                }
            })
    
        let data = await response.json();
        console.log(data)
        // 圖片
        // console.log(data["data"]["data"]['trip']["attraction"]["image"])
        new_order_card_img.style.backgroundImage=`url('${data["data"]["data"]['trip']["attraction"]["image"]}')`
        document.querySelector(`#order_info_contain_${i}`).appendChild(new_order_card_img)



        
    }
}
getOrderInfo()





async function change_img_table(){
    let table_background = document.createElement('div')
    table_background.className='signin_table_background'
    document.querySelector(`.body`).prepend(table_background);
    // console.log("123")


    //登入頁
    signin_table_dom = document.createElement('div')
    signin_table_dom.className='signin_enter'
    document.querySelector(`.signin_table_background`).prepend(signin_table_dom);
  
    // 創建登入頁上方藍色區塊
    signin_table_dom = document.createElement('div');
    signin_table_dom.className = 'signin_enter__top signin_enter__top--coler1';
    document.querySelector('.signin_enter').prepend(signin_table_dom);
  
    // 創建下方內容範圍大區塊
    signin_table_dom = document.createElement('div');
    signin_table_dom.className = 'user_upload_img_area';
    document.querySelector('.signin_enter').appendChild(signin_table_dom);
  
    // 創建下方標題範圍區塊
    signin_table_dom = document.createElement('div');
    signin_table_dom.className = 'signin_input_area_title_area';
    document.querySelector('.user_upload_img_area').appendChild(signin_table_dom);
  
    // 創建登入頁標題
    signin_table_dom = document.createElement('div');
    signin_table_dom.textContent='請上傳新的圖片'
    signin_table_dom.className = 'signin_input_area_title_area__title signin_input_area_title_area__title--fontcoler1';
    document.querySelector('.signin_input_area_title_area').appendChild(signin_table_dom);
  
    // 創建登入頁 右邊關閉X
    signin_table_dom = document.createElement('div');
    signin_table_dom.className = 'signin_input_area_title_area__close';

    //關閉登入頁
    signin_table_dom.addEventListener('click', () => {
      let remove_dom = document.querySelector(`.signin_table_background`)
      remove_dom.remove();
    })
    document.querySelector('.signin_input_area_title_area').appendChild(signin_table_dom);

    // 上傳照片的限制說明
    let upload_limit = document.createElement("div")
    upload_limit.textContent='請上傳小於15mb之png圖片'
    upload_limit.id="upload_limit"
    document.querySelector('.user_upload_img_area').appendChild(upload_limit);

    // 上傳照片的按鈕
    let upload_butt = document.createElement("input")
    upload_butt.type='file'
    upload_butt.id="file-uploader"
    upload_butt.accept='image/png'
    document.querySelector('.user_upload_img_area').appendChild(upload_butt);

    // 預覽照片
    let upload_img_view = document.createElement("div")
    upload_img_view.id ="preview"
    upload_img_view.style ="max-width: 300px; max-height: 300px;"
    upload_img_view.type='file'
    upload_img_view.accept='image/png'
    document.querySelector('.user_upload_img_area').appendChild(upload_img_view);


    let upload_img_butt = document.createElement("button")
    upload_img_butt.style ="max-width: 100px; min-height: 30px; "
    upload_img_butt.id = "upload_img_butt"
    upload_img_butt.textContent='確定更換'
    upload_img_butt.disabled="false"
    upload_img_butt.style.backgroundColor='gray'
    upload_img_butt.style.cursor='not-allowed'

    upload_img_butt.addEventListener('click', () => {
        console.log("123")

        const fileUploader = document.querySelector('#file-uploader');
        const upfiles = fileUploader.files[0];
    
        // 監聽「取得 Base64」按鈕
        if (!upfiles) {
            console.log('請先選擇一個 PNG 檔案');
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            const base64String = e.target.result;
            console.log(base64String);
            updata_img(base64String)

        };
        reader.readAsDataURL(upfiles); // 把檔案讀成 Base64


    })

    document.querySelector('.user_upload_img_area').appendChild(upload_img_butt);
    upload_img_but_click()
}





// 上傳個人圖片點擊上傳
// async function upload_img_but_click(){
//     const fileUploader = document.querySelector('#file-uploader');
//     const previewImage = document.querySelector('#preview'); // 取得預覽圖片的元素
    
//     fileUploader.addEventListener('change', (e) => {
//        console.log(e.target.files); // get list of file objects
//        const files = e.target.files; // 取得選取的文件列表
    
//        if (files && files.length > 0) { // 確保有選取文件
//             display_img(files); // 調用 display_img 函式來預覽
//             let upload_img_butt = document.createElement("button")
//                 let but_dom = document.querySelector('#upload_img_butt');
//                 but_dom.removeAttribute('disabled');
//                 but_dom.style.backgroundColor='rgb(66, 134, 151)'
//                 but_dom.style.cursor='pointer'
    
//        }
//     });
// }

// 上傳個人圖片點擊上傳(限制檔案大小)
async function upload_img_but_click() {
    const fileUploader = document.querySelector('#file-uploader');
    const previewImage = document.querySelector('#preview'); // 取得預覽圖片的元素

    fileUploader.addEventListener('change', (e) => {
        console.log(e.target.files);
        const files = e.target.files;

        if (files && files.length > 0) { // 確保有選取文件

            const file = files[0];
            const maxSizeInMB = 15;
            const maxSizeInBytes = maxSizeInMB * 1024 * 1024;

            if (file.size > maxSizeInBytes) {
                alert(`檔案太大了！請選擇小於 ${maxSizeInMB}MB 的圖片。`);
                fileUploader.value = ""; // 如果圖片太大張清空路徑
                return;
            }

            display_img(files);

            let upload_img_butt = document.createElement("button")
            let but_dom = document.querySelector('#upload_img_butt');
            but_dom.removeAttribute('disabled');
            but_dom.style.backgroundColor = 'rgb(66, 134, 151)';
            but_dom.style.cursor = 'pointer';
        }
    });
}

async function updata_img(base64String){
        // 用POST發送請求到連結
        let response = await fetch("/api/user_img_upload",
            {
            method:"POST",
            headers: {
                'content-type': 'application/json',
                "Authorization": `Bearer ${localStorage.getItem('token')}`
            },

            //發送請求到後方並戴上這些json
            body:JSON.stringify({"img":base64String,})

            })
            //從後端接資料過來
            let data =await response.json();

            console.log(data)
    
            window.location.reload();
}


async function change_password(){
    let table_background = document.createElement('div')
    table_background.className='signin_table_background'
    document.querySelector(`.body`).prepend(table_background);
    // console.log("123")


    //登入頁
    signin_table_dom = document.createElement('div')
    signin_table_dom.className='signin_enter'
    document.querySelector(`.signin_table_background`).prepend(signin_table_dom);
  
    // 創建登入頁上方藍色區塊
    signin_table_dom = document.createElement('div');
    signin_table_dom.className = 'signin_enter__top signin_enter__top--coler1';
    document.querySelector('.signin_enter').prepend(signin_table_dom);
  
    // 創建下方內容範圍大區塊
    signin_table_dom = document.createElement('div');
    signin_table_dom.className = 'user_upload_img_area';
    document.querySelector('.signin_enter').appendChild(signin_table_dom);
  
    // 創建下方標題範圍區塊
    signin_table_dom = document.createElement('div');
    signin_table_dom.className = 'signin_input_area_title_area';
    document.querySelector('.user_upload_img_area').appendChild(signin_table_dom);
  
    // 創建登入頁標題
    signin_table_dom = document.createElement('div');
    signin_table_dom.textContent='變更密碼'
    signin_table_dom.className = 'signin_input_area_title_area__title signin_input_area_title_area__title--fontcoler1';
    document.querySelector('.signin_input_area_title_area').appendChild(signin_table_dom);
  
    // 創建登入頁 右邊關閉X
    signin_table_dom = document.createElement('div');
    signin_table_dom.className = 'signin_input_area_title_area__close';

    //關閉登入頁
    signin_table_dom.addEventListener('click', () => {
      let remove_dom = document.querySelector(`.signin_table_background`)
      remove_dom.remove();
    })
    document.querySelector('.signin_input_area_title_area').appendChild(signin_table_dom);


    // 變更密碼的輸入框標題
    let update_password_title = document.createElement("div")
    update_password_title.id="update_password_title"
    update_password_title.textContent='舊密碼'
    document.querySelector('.user_upload_img_area').appendChild(update_password_title);
    
    // 變更密碼的輸入框
    let update_password_input = document.createElement("input")
    update_password_input.type='password'
    update_password_input.id="update_password_input"
    document.querySelector('.user_upload_img_area').appendChild(update_password_input);



    // 變更新密碼的輸入框標題
    let update_new_password_title = document.createElement("div")
    update_new_password_title.id="update_new_password_title"
    update_new_password_title.textContent='新密碼'
    document.querySelector('.user_upload_img_area').appendChild(update_new_password_title);
    
    // 變更新密碼的輸入框
    let update_new_password_input = document.createElement("input")
    update_new_password_input.type='password'
    update_new_password_input.id="update_new_password_input"
    document.querySelector('.user_upload_img_area').appendChild(update_new_password_input);
    

    // 變更新密碼的按鈕
    let update_new_password_butt = document.createElement("button")
    update_new_password_butt.id="update_new_password_butt"
    update_new_password_butt.textContent='確定變更'
    document.querySelector('.user_upload_img_area').appendChild(update_new_password_butt);

    update_new_password_butt.addEventListener('click', async() => {
        if(update_password_input.value==''){
            update_password_input.style.borderColor='red'
        }else{
            update_password_input.style.borderColor='unset'
        }

        if(update_new_password_input.value==''){
            update_new_password_input.style.borderColor='red'
        }else{
            update_new_password_input.style.borderColor='unset'
        }

        if(update_password_input.value!='' & update_new_password_input.value!=''){
            console.log('ok')


            let response = await fetch("/api/user_password_update",
                {
                method:"POST",
                headers: {
                    'content-type': 'application/json',
                    "Authorization": `Bearer ${localStorage.getItem('token')}`
                },
    
                //發送請求到後方並戴上這些json
                body:JSON.stringify({"old_password":update_password_input.value,
                                     "new_password":update_new_password_input.value,
                })
    
                })
                //從後端接資料過來
                let data =await response.json();
    
                console.log(data)
                if(data['ok']==true){
                    // console.log(data)
                    localStorage.clear('token')

                    if(document.querySelector("#error_message")){
                        document.querySelector("#error_message").remove()
                        let error_message = document.createElement("div")
                        error_message.textContent= "密碼變更成功將自動跳轉，請重新登入"
                        error_message.class = "error_message"
                        error_message.id = "error_message"
                        document.querySelector(".user_upload_img_area").appendChild(error_message)

                    }else{
                        let error_message = document.createElement("div")
                        error_message.textContent= "密碼變更成功將自動跳轉，請重新登入"
                        error_message.class = "error_message"
                        error_message.id = "error_message"
                        document.querySelector(".user_upload_img_area").appendChild(error_message)
                    }

                    setTimeout("window.location.href = `/`",1000)


                }else{
                    if(document.querySelector("#error_message")){
                        document.querySelector("#error_message").remove()
                        let error_message = document.createElement("div")
                        error_message.textContent= data['message']
                        error_message.class = "error_message"
                        error_message.id = "error_message"
                        document.querySelector(".user_upload_img_area").appendChild(error_message)

                    }else{
                        let error_message = document.createElement("div")
                        error_message.textContent= data['message']
                        error_message.class = "error_message"
                        error_message.id = "error_message"
                        document.querySelector(".user_upload_img_area").appendChild(error_message)
                    }
                }





        }
        




    })



}



