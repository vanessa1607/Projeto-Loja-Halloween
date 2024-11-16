import json

class Produto:  #genérico
    def __init__(self,nome,preco,quantidade):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

    def exibir_dados(self):
        print(f'Nome {self.nome} , Preço: {self.preco:.2f} , Quantidade: {self.quantidade:.2f}')
        
    def to_dict(self):
        return {
            'tipo': 'Produto',
            'nome': self.nome,
            'preco': self.preco,
            'quantidade': self.quantidade
        }

    @staticmethod
    def to_produto(dic_produto):
        return Produto(dic_produto['nome'], dic_produto['preco'], dic_produto['quantidade'])


def vender_produto(lista):
    nome = input("Digite o nome do produto que deseja comprar: ").capitalize()
    quantidade_venda = int(input("Insira a quantidade que deseja comprar: "))
        
    for produto in lista:
        if produto.nome == nome:
            if produto.quantidade >= quantidade_venda:
                produto.quantidade-= quantidade_venda
                total_preco = produto.preco * quantidade_venda
                print(f"Venda {nome} registada com sucesso Total: {total_preco:.2f} Quantidade: {quantidade_venda}")
                break
            else:
                print("Stock insuficiente")
    else:
        print(f"Produto {nome} não encontrado")


class ProdutoEletronico(Produto):
    def __init__(self, nome, preco, quantidade,garantia):
        super().__init__(nome, preco, quantidade)
        self.garantia = garantia

    def exibir_dados(self):
        super().exibir_dados()
        print(f"Garantia: {self.garantia}")

    def to_dict(self):
        data = super().to_dict()
        data['tipo'] = 'Eletronico'
        data['garantia'] = self.garantia
        return data
    @staticmethod
    def to_eletronico(dic_produto):
        return ProdutoEletronico(dic_produto['nome'], dic_produto['preco'], dic_produto['quantidade'],dic_produto['garantia'])


class ProdutoRoupas(Produto):
    def __init__(self, nome, preco, quantidade,tamanho):
        super().__init__(nome, preco, quantidade)
        self.tamanho = tamanho

    def exibir_dados(self):
        super().exibir_dados()
        print(f"Tamanho: {self.tamanho}")

    def to_dict(self):
        data = super().to_dict()
        data['tipo'] = 'Roupas'
        data['tamanho'] = self.tamanho
        return data
    @staticmethod
    def to_roupas(dic_produto):
        return ProdutoRoupas(dic_produto['nome'], dic_produto['preco'], dic_produto['quantidade'],dic_produto['tamanho'])

def novo_produto(lista):
    nome = input('Digite o produto:').capitalize()
    for produto in lista:
        if produto.nome == nome:
            print("Este produto ja existe na listagem.")
            produto.exibir_dados()
            quantidade = int(input("Digite a quantidade que deseja acrescentar: "))
            produto.quantidade += quantidade
            print("Quantidade atualizada com sucesso")
            
            opcao = int(input("Deseja alterar o preço existente? 1-Sim 2-Não : "))
            if opcao == 1:
                preco = float(input("Digite o atual valor do produto: "))
                produto.preco = preco
                print ("Preço atualizado com sucesso")
                break
            else:
                print(f"O preço irá se manter a {produto.preco:.2f}")
                break
        
    else:
        preco = float(input('Digite o preço:'))
        quantidade = int(input('Digite a quantidade:'))
        print('1.Eletrônico 2.Roupas 3.Outro')
        tipo = valida_valor(1,3)
        if tipo == 1:
            garantia = int(input("Insira a garantia (em meses): "))
            produto = ProdutoEletronico(nome,preco,quantidade,garantia)
        elif tipo == 2:
            tamanho = input("Insira o tamanho que deseja: (XS,S,M,L,XL,XXL)")
            produto = ProdutoRoupas(nome,preco,quantidade,tamanho)
        else:
            produto = Produto(nome,preco,quantidade)
        lista.append(produto)
        print(f"Produto {nome} inserido com sucesso")


def valida_valor(min,max):
   while True:
      try:
        a= int(input(f"digite valor entre {min} e {max}: "))
        if a>min-1 and a <max+1:
            return a
      except ValueError:
          print(f"Erro: Precisa digitar um número válido entre {min} e {max}")
          
   
def mostra_produtos(lista):
    for produto in lista:
        produto.exibir_dados()

def repor_quantidade(lista):
    nome = input("Digite o nome do produto que deseja repor: ").capitalize()
  
    for produto in lista:
        if produto.nome == nome:
            quantidade_repor = int(input("Insira a quantidade que quer repor: "))
            produto.quantidade += quantidade_repor
            print(f"No produto {nome} foi atualizada com sucesso com quantidade de {quantidade_repor}")
            break
    else:
        print(f"Produto {nome} não encontrado")

def procurar_produto(lista):

    nome = input("Digite o nome do produto que deseja procurar: ").capitalize()

    for produto in lista:
        if produto.nome == nome:
            produto.exibir_dados()
            break
    else:
        print(f"Produto {nome} não encontrado")


def salvar_produtos(lista):
    arquivo = 'produtos_loja.json'
    with open(arquivo, 'w') as f:
        #json.dump([funcionario.to_dict() for funcionario in lista], f, indent=4)
        lista_dic=[]
        for produto in lista:
            d_produto = produto.to_dict()
            lista_dic.append(d_produto)
        json.dump(lista_dic,f,indent=4)
    print(f'Produtos salvos em {arquivo} com sucesso!')



def carregar_produtos():
    arquivo = 'produtos_loja.json'
    try:
        with open(arquivo, 'r') as f:
            lista_produtos = json.load(f)
            #lista = [to_funcionario(item) for item in lista_dicio]
            produtos=[]
            for dicionario in lista_produtos:
                if dicionario["tipo"]== "Produto":
                    f1=Produto.to_produto(dicionario)
                    #funcionarios.append(f1)
                elif dicionario["tipo"]== "Eletronico":
                    f1=ProdutoEletronico.to_eletronico(dicionario)
                    #funcionarios.append(f1)
                else:
                    f1=ProdutoRoupas.to_roupas(dicionario)
                    #funcionarios.append(f1)
                produtos.append(f1)
            return produtos
    except FileNotFoundError:
        print(f"Arquivo {arquivo} não encontrado. Iniciando uma lista vazia.")
        return []
        


def main():
    lista_produtos = carregar_produtos()
    while True:
        op=menu()
        match op :
            case 1:
                novo_produto(lista_produtos)
            case 2:
                mostra_produtos(lista_produtos)
            case 3:
                vender_produto(lista_produtos)
            case 4:
                repor_quantidade(lista_produtos)
            case 5:
                procurar_produto(lista_produtos)
            case 6:
                salvar_produtos(lista_produtos)
                print("saindo...")
                break
        

def menu():
    print('1 - Inserir produto')
    print('2 - Exibir dados dos produtos')
    print('3 - Vender produto')
    print('4 - Repor Stock')
    print('5 - Encontrar um produto específico')
    print('6 - Sair')

    while True:
        try:
            op= int(input('Digite a opcao de 1 a 6:'))
            if op>0 and op<7:
                break
        except ValueError:
            print("Opção inválida! Por favor, escolha um número de 1 a 6.")
    return op

if __name__ == "__main__":
    main()
