
let now_page;
let have_page;
let keyword2;

let right_but_maxclick_times=0
let now_move_width = 0
// 捷運list_bar_but點擊
// 設定最大最小的position寬度
// 設定最右邊的點擊次數



//將現有頁面變數重製
function page_refresh(){
    now_page = 0;
    have_page =[];
    have_page.push(0);
  };

//關鍵字更新
function keyword_update(){
    keyword2 = document.querySelector("#search_input").value
  };



// 1.景點關鍵字搜尋功能
function att_search_but_click(){
    search_text = document.querySelector("#search_input").value
    // 先清空現有的景點卡片
    let web_att_card = document.querySelectorAll('.attraction_area_box');
    for(let n =0 ; n<web_att_card.length; n++){
        web_att_card[n].remove()
        };

    page_refresh()
    keyword_update()
    get_attraction_data(now_page,search_text) //新增搜尋關鍵字的卡片
    }


// 2.捷運站列表左按鈕
// 這邊把他修改成根據畫面的寬度去做百分比的按鈕功能
// 每次都移動現有寬度10%的內容
// 然後計算極限值的寬度，不能超過這個寬度
let mrt_bar_click_times = 0;
function click_right_times(){
    mrt_bar_click_times+=1;
}
function click_left_times(){
    mrt_bar_click_times-=1;
}

// // 3.捷運站列表左按鈕
// function list_bar_left_but_click(){
//     //先檢視網頁寬度，再根據寬度去計算最多可以按幾次按鈕
//     let body_dom = document.querySelector(".body");
//     let body_dom_width = body_dom.offsetWidth; //
//     // console.log(body_dom_width)
//     move_pixel = body_dom_width/10
//     show_pixel = move_pixel*mrt_bar_click_times

//     if(now_move_width<0){
//       mrt_item_dom =  document.querySelectorAll(".list_bar_inner_content_mrt");
//       now_move_width += move_pixel

//       for(i=0;i<mrt_item_dom.length;i++){
//         mrt_item_dom[i].style.left =  `${now_move_width}px`
//         mrt_item_dom[i].style.transform = `translateX(${-580 * mrt_bar_click_times}px)`;
//       };
//     }
//   }


// // 3.捷運站列表右按鈕
// function list_bar_right_but_click(){
//     let body_dom = document.querySelector(".body");
//     let body_dom_width = body_dom.offsetWidth;
//     // console.log(body_dom_width)
//     let max_width;

//     if(body_dom_width<360){
//       max_width = -1600;
//     }else{
//       max_width = -670;
//     };
    
//     if(now_move_width > max_width){
//       mrt_item_dom =  document.querySelectorAll(".list_bar_inner_content_mrt");
//       now_move_width-=60

//       for(i=0;i<mrt_item_dom.length;i++){
//         mrt_item_dom[i].style.left =  `${now_move_width}px`
//         mrt_item_dom[i].style.transform = `translateX(${-30 * Math.abs(now_move_width/30)}px)`;
//       };
//     };
//   };
