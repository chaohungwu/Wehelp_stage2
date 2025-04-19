

// 以下提供必填 CCV 以及選填 CCV 的 Example
// 必填 CCV Example
var fields = {
    number: {
        element: '.form-control.card-number',
        placeholder: '**** **** **** ****'
    },
    expirationDate: {
        element: document.getElementById('tappay-expiration-date'),
        placeholder: 'MM / YY'
    },
    ccv: {
        // element: $('.form-control.ccv')[0],
        element: document.getElementById('cvv_input'),
        placeholder: 'CVV'
    }
}
// 選填 CCV Example
// var fields = {
//     number: {
//         // css selector
//         element: '#card-number',
//         placeholder: '**** **** **** ****'
//     },
//     expirationDate: {
//         // DOM object
//         element: document.getElementById('card-expiration-date'),
//         placeholder: 'MM / YY'
//     }
// }
console.log(fields)


// 輸入內容的辨識樣式
TPDirect.card.setup({
    fields: fields,
    styles: {
        // Style all elements
        'input': {
            'color': 'gray'
        },

        // Styling ccv field
        'input.ccv_input': {
            'font-size': '16px',
        },

        // Styling expiration-date field
        'input.expiration-date': {
            'font-size': '16px'
        },

        // Styling card-number field
        'input.card-number': {
            'font-size': '16px'
          },

        // style focus state
        ':focus': {
            'color': 'black'
        },

        // style valid state
        '.valid': {
            'color': 'green'
        },

        // style invalid state
        '.invalid': {
            'color': 'red'
        },
        
        // Media queries
        // Note that these apply to the iframe, not the root window.
        '@media screen and (max-width: 400px)': {
            'input': {
                'color': 'orange'
            }
        }
    },

    // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
        beginIndex: 6, 
        endIndex: 11
    }
})


TPDirect.card.onUpdate(function (update) {
    // update.canGetPrime === true
    // --> you can call TPDirect.card.getPrime()
    if (update.canGetPrime) {
        // Enable submit Button to get prime.
        // submitButton.removeAttribute('disabled')
        // $('button[type="submit"]').removeAttr('disabled')
        document.querySelector("#sum_booking_info_contain_BuyButt").removeAttribute('disabled')
    } else {
        // Disable submit Button to get prime.
        // submitButton.setAttribute('disabled', true)
        // $('button[type="submit"]').attr('disabled', true)
        // document.querySelector("#sum_booking_info_contain_BuyButt").attribute('disabled', true)
        document.querySelector("#sum_booking_info_contain_BuyButt").disabled = true
    }

    // cardTypes = ['visa', 'mastercard', ...]
    // var newType = update.cardType === 'unknown' ? '' : update.cardType
    // $('#cardtype').text(newType)
    // document.querySelector("#cardtype").textContent = newType

    
    /* Change form-group style when tappay field status change */
    /* ======================================================= */
    // number 欄位是錯誤的
    if (update.status.number === 2) {
        // setNumberFormGroupToError('.card-number-group')
    } else if (update.status.number === 0) {
        // setNumberFormGroupToSuccess('.card-number-group')
    } else {
        // setNumberFormGroupToNormal('.card-number-group')
    }
    

    if (update.status.expiry === 2) {
        // setNumberFormGroupToError('.expiration-date-group')
    } else if (update.status.expiry === 0) {
        // setNumberFormGroupToSuccess('.expiration-date-group')
    } else {
        // setNumberFormGroupToNormal('.expiration-date-group')
    }
    

    if (update.status.ccv === 2) {
        // setNumberFormGroupToError('.ccv-group')
    } else if (update.status.ccv === 0) {
        // setNumberFormGroupToSuccess('.ccv-group')
    } else {
        // setNumberFormGroupToNormal('.ccv-group')
    }
})


// call TPDirect.card.getPrime when user submit form to get tappay prime
// $('form').on('submit', onSubmit)

let order_requset;

function onSubmit(event) {
    event.preventDefault()

    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()

    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        alert('請輸入正確的付款資訊')



        return
    }

    // Get prime
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            alert('get prime error ' + result.msg)
            return
        };
        // 取得prime
        // alert('get prime 成功，prime: ' + result.card.prime)
        // send prime to your server, to pay with Pay by Prime API .
        // Pay By Prime Docs: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api

        let order_price;
        let attraction_info;
        let order_date;
        let order_time;
        let contact_name;
        let contact_email;
        let contact_phone;
        let order_requset;

        // 取得資訊
        async function pay_the_order(){
            let booking_info = await get_booking_info();
            console.log(booking_info)

            order_price = booking_info['data']['data']['price']
            attraction_info = booking_info['data']['data']['attraction']
            order_date = booking_info['data']['data']['date']
            order_time = booking_info['data']['data']['time']
            contact_name = document.querySelector("#Name_input").value
            contact_email = document.querySelector("#mail_input").value
            contact_phone = document.querySelector("#phone_input").value

            order_requset={
                            "prime": result.card.prime,
                            "order": {
                                "price": order_price,
                                "trip": {
                                    "attraction": attraction_info,
                                    "date": order_date,
                                    "time": order_time
                                        },
                                "contact": {
                                    "name": contact_name,
                                    "email": contact_email,
                                    "phone": contact_phone
                                        }
                                    }
                            }

            // 將prime傳到到後端
            let response = await fetch("/api/orders", {
                method: 'POST',
                headers: {
                        "Authorization": `Bearer ${localStorage.getItem('token')}`
                        },
                body:JSON.stringify(order_requset)
                
                                });

            // console.log(order_requset)
            let data = await response.json();
            console.log(data) //回傳到前端的資料
            

            let order_num = data['data']['number']
            window.location.href = `/thankyou?number=${order_num}` //跳轉到thankyou頁面


            return order_requset
        }

        pay_the_order();



    })
}


