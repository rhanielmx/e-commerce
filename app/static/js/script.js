

onClickCar = (product, price) =>{
    var nome = document.getElementById(product)
    var preco = document.getElementById(price)

    let venda = {'Product': nome, 'Price': preco}

    Cookies.set('Carrinho', venda)
    alert("Adicionado com Sucesso")

}   
onClickCarDel = (product) =>{
    Cookies.remove(product)
    window.location.reload()
}


