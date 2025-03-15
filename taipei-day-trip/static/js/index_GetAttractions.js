async function get_user_message(){

    //利用fetch進行連線並取得資料
    fetch(`/api/attractions?page=${page}&keyword=${keyword}`,{method:'GET'}).then(function(response){
        // 得到json格式的response 
        return response.json();
        }).then(function(response_data){

        console.log(response_data)
    


    };
    };