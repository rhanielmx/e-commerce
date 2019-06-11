

onClickCar = (product, price) =>{
    var nome = document.getElementById(product)
    var preco = document.getElementById(price)
    Cookies.set(nome.innerHTML, preco.innerHTML)

}   
onClickCarDel = (product) =>{
    var nome = document.getElementById(product)
    Cookies.remove(nome.innerHTML)

}

