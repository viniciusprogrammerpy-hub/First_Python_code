import os

print('olá usuario')
nome = input('digite seu nome: ')
print(f'seja bem vindo, {nome}!')
idade = input('digite sua idade: ')

if not idade.isnumeric():
    print('idade inválida, digite apenas números')
else:
    if int(idade) < 18:
        print('você é menor de idade')
    else:
        print('você é maior de idade')
        readline = input('você é maior de idade, deseja continuar? (s/n): ')
        if readline.lower() == 's':
            print('continuando')
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                print("A variável de ambiente OPENAI_API_KEY não está definida.")
                raise SystemExit(1)

            from openai import OpenAI

            client = OpenAI(api_key=api_key)
            response = client.responses.create(
                model="gpt-4o-mini",
                input=input('digite sua pergunta: '),
            )
            print(response.output_text)
        elif readline.lower() == 'n':
            print('ok, até mais!')
