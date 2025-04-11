
// 登入與註冊畫面
async function signin_enter(){
    //1. 建立DOM
    //外底部灰色
    let signin_table_dom = document.createElement('div')
    signin_table_dom.className='signin_table_background'
    document.querySelector(`.body`).prepend(signin_table_dom);
  
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
    signin_table_dom.className = 'signin_input_area';
    document.querySelector('.signin_enter').appendChild(signin_table_dom);
  
    // 創建下方標題範圍區塊
    signin_table_dom = document.createElement('div');
    signin_table_dom.className = 'signin_input_area_title_area';
    document.querySelector('.signin_input_area').appendChild(signin_table_dom);
  
    // 創建登入頁標題
    signin_table_dom = document.createElement('div');
    signin_table_dom.textContent='登入會員帳號'
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
  
    // 創建email輸入欄
    signin_table_dom = document.createElement('input');
    signin_table_dom.className = 'signin_input_area__EmailInput';
    signin_table_dom.type='text'
    signin_table_dom.placeholder='輸入電子信箱'
    document.querySelector('.signin_input_area').appendChild(signin_table_dom);
  
    // 創建密碼輸入欄
    signin_table_dom = document.createElement('input');
    signin_table_dom.className = 'signin_input_area__PasswordInput';
    signin_table_dom.type='password'
    signin_table_dom.placeholder='輸入密碼'
    document.querySelector('.signin_input_area').appendChild(signin_table_dom);
  
    // 創建登入按鈕
    signin_table_dom = document.createElement('button');
    signin_table_dom.className = 'signin_input_area__signinButt';
    signin_table_dom.textContent='登入帳戶'
    signin_table_dom.addEventListener('click', () => {
      signin()
    })
    document.querySelector('.signin_input_area').appendChild(signin_table_dom);
  
    // 創建註冊連結
    signin_table_dom = document.createElement('div');
    signin_table_dom.className = 'signin_input_area__SignupText';
    signin_table_dom.textContent='還沒有帳戶？點此註冊'
    signin_table_dom.addEventListener('click', () => {
      let remove_dom = document.querySelector(`.signin_table_background`)
      remove_dom.remove();
      signup_enter();
    })
    document.querySelector('.signin_input_area').appendChild(signin_table_dom);
  
    //創建登入成功或是登入失敗訊息的框
    signin_table_dom = document.createElement('div');
    signin_table_dom.className = 'signin_singup_state';
  
    document.querySelector('.signin_input_area').appendChild(signin_table_dom);
  
  
  }
  
  //註冊介面
async function signup_enter(){
    //1. 建立DOM
    //外底部灰色
    let signin_table_dom = document.createElement('div')
    signin_table_dom.className='signin_table_background'
    document.querySelector(`.body`).prepend(signin_table_dom);
  
    //註冊頁
    signin_table_dom = document.createElement('div')
    signin_table_dom.className='signup_enter'
    document.querySelector(`.signin_table_background`).prepend(signin_table_dom);
  
    // 創建註冊頁上方藍色區塊
    signin_table_dom = document.createElement('div');
    signin_table_dom.className = 'signin_enter__top signin_enter__top--coler1';
    document.querySelector('.signup_enter').prepend(signin_table_dom);
  
    // 創建下方內容範圍大區塊
    signin_table_dom = document.createElement('div');
    signin_table_dom.className = 'signin_input_area';
    document.querySelector('.signup_enter').appendChild(signin_table_dom);
  
    // 創建下方標題範圍區塊
    signin_table_dom = document.createElement('div');
    signin_table_dom.className = 'signin_input_area_title_area';
    document.querySelector('.signin_input_area').appendChild(signin_table_dom);
  
    // 創建註冊頁標題
    signin_table_dom = document.createElement('div');
    signin_table_dom.textContent='註冊會員帳號'
    signin_table_dom.className = 'signin_input_area_title_area__title signin_input_area_title_area__title--fontcoler1';
    document.querySelector('.signin_input_area_title_area').appendChild(signin_table_dom);
  
    // 創建註冊頁 右邊關閉X
    signin_table_dom = document.createElement('div');
    signin_table_dom.className = 'signin_input_area_title_area__close';
      //關閉註冊頁
      signin_table_dom.addEventListener('click', () => {
      let remove_dom = document.querySelector(`.signin_table_background`)
      remove_dom.remove();
    })
    document.querySelector('.signin_input_area_title_area').appendChild(signin_table_dom);
  
    // 創建註冊姓名輸入欄
    signin_table_dom = document.createElement('input');
    signin_table_dom.className = 'signup_input_area__NameInput';
    signin_table_dom.type='text'
    signin_table_dom.placeholder='輸入姓名'
    document.querySelector('.signin_input_area').appendChild(signin_table_dom);
  
    // 創建註冊email輸入欄
    signin_table_dom = document.createElement('input');
    signin_table_dom.className = 'signup_input_area__EmailInput';
    signin_table_dom.type='text'
    signin_table_dom.placeholder='輸入電子郵件'
    document.querySelector('.signin_input_area').appendChild(signin_table_dom);
  
    // 創建註冊密碼輸入欄
    signin_table_dom = document.createElement('input');
    signin_table_dom.className = 'signup_input_area__PasswordInput';
    signin_table_dom.type='password'
    signin_table_dom.placeholder='輸入密碼'
    document.querySelector('.signin_input_area').appendChild(signin_table_dom);
  
    // 創建送出鈕
    signin_table_dom = document.createElement('button');
    signin_table_dom.className = 'signup_input_area__signinButt';
    signin_table_dom.textContent='註冊'
    signin_table_dom.addEventListener('click', () => {
      signup();
    })
    document.querySelector('.signin_input_area').appendChild(signin_table_dom);
  
    // 創建登入連結
    signin_table_dom = document.createElement('div');
    signin_table_dom.className = 'signup_input_area__SignupText';
    signin_table_dom.textContent='已經有帳戶？點此登入'
    signin_table_dom.addEventListener('click', () => {
      let remove_dom = document.querySelector(`.signin_table_background`)
      remove_dom.remove();
      signin_enter();
    })
    document.querySelector('.signin_input_area').appendChild(signin_table_dom);
  
    //創建註冊成功或是註冊失敗訊息
    signin_table_dom = document.createElement('div');
    signin_table_dom.className = 'signup_singup_state';
    document.querySelector('.signin_input_area').appendChild(signin_table_dom);
  
  }
  
  //01.註冊新會員
async function signup(){
    let signup_name = document.querySelector(".signup_input_area__NameInput").value;
    let signup_email = document.querySelector(".signup_input_area__EmailInput").value;
    let signup_password = document.querySelector(".signup_input_area__PasswordInput").value;
  
    // 用POST發送請求到連結
    let response = await fetch("/api/user",
        {
            method:"POST",
            //發送請求到後方並戴上這些json
            body:JSON.stringify({"name":signup_name,
                                 "email":signup_email,
                                 "password":signup_password})
            })
            //從後端接資料過來
            let data =await response.json();
            if(data["ok"]==true){
              // window.alert("註冊成功");
              document.querySelector('.signup_singup_state').textContent = `註冊成功`
              document.querySelector('.signup_enter').style.height='365px'
              setTimeout("window.location.href = `/`",1000)
            //   window.location.href = `/`

            }else{
              document.querySelector('.signup_singup_state').textContent = data["message"]
              document.querySelector('.signup_enter').style.height='365px'
            }
      }
  
  //02.登入會員
async function signin(){
    let signin_email = document.querySelector(".signin_input_area__EmailInput").value;
    let signin_password = document.querySelector(".signin_input_area__PasswordInput").value;
  
    let response = await fetch("/api/auth",
        {
          method:"PUT",
          //發送請求到後方並戴上這些json
          //加上這一串後會將BODY中的東西以json格式傳到後端，但是在fastapi中會自動轉為dict，這邊要注意
          headers: {
          'Content-Type': 'application/json', // 指定發送的資料格式為 JSON
          },
  
          body:JSON.stringify({"email":signin_email,
                               "password":signin_password})
        })
  
        let data = await response.json();
  
        if(data['error']==true){
          document.querySelector('.signin_singup_state').textContent = `${data['message']}`
          document.querySelector('.signin_enter').style.height='300px'
          // alert(data['message']);
  
        }else if(data['token']!= undefined){
          let token = data['token'];
          // sessionStorage.setItem('token', token);
          localStorage.setItem('token', token);
          document.querySelector('.signin_singup_state').textContent = `登入成功`
          document.querySelector('.signin_enter').style.height='300px'
  
          setTimeout("window.location.reload();",1000)
          // alert('登入成功');
          // window.location.href = `/`
  
        }
      }
  
//03.登入狀態確認
async function signin_license_check(){
  let response = await fetch(`/api/auth`,
        {
          method:'GET',
          headers: {
          "Authorization": `Bearer ${localStorage.getItem('token')}`
          }
        })
          let data = await response.json();
          let user_info = data['data']

          // 登入失敗就回到首頁
            if(user_info==null){
              singin_dom = document.querySelector("#singin_enter")
              singin_dom.textContent='登入/註冊'

            }else{
              // 將使用者名稱也存在localstorage(booking頁面使用)
              localStorage.setItem('user_name', user_info["name"]);

              singin_dom = document.querySelector("#singin_enter")
              singin_dom.textContent='登出系統'
              singin_dom.addEventListener('click', () => {
                localStorage.clear('token')
                document.querySelector('.signin_table_background').remove()

                window.location.reload();

                })
            }
          
            return user_info
        }
signin_license_check()
