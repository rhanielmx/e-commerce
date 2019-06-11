

onClickCar = (product, price) =>{
    var nome = document.getElementById(product)
    var preco = document.getElementById(price)
    Cookies.set(nome.innerHTML, preco.innerHTML)
    alert("Adicionado com Sucesso")

}   
onClickCarDel = (product) =>{
    Cookies.remove(product)
    window.location.reload()
}


