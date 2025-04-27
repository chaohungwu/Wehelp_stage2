function loading_view_create(){
    loading_view_backgraund = document.createElement('div');
    loading_view_backgraund.className="loading_page_contain"

    document.querySelector('body').prepend(loading_view_backgraund)
}


function loading_view_remove(){
    // document.querySelector('')
}

loading_view_create()

setTimeout(loading_view_remove())

