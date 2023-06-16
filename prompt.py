import cmd

class Prompt(cmd.Cmd):
    prompt = '>> '

    def do_hello(self, args):
        """Comando para dizer olá"""
        print('Olá!')

    def do_quit(self, args):
        """Comando para sair do prompt"""
        print('Saindo do prompt...')
        return True

    def default(self, line):
        if line.lower() == 'bye':
            print('Até logo!')
            return True
        else:
            print('Comando inválido.')

if __name__ == '__main__':
    prompt = Prompt()
    prompt.cmdloop('Iniciando prompt de comando...')