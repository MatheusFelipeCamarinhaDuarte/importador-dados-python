class Correcao():
    def __init__(self):
        pass

    def corrigir_nome_acentos(self,nome:str) -> str:
        """Método para retirar caracteres especiais de dentro de uma string

        Args:
            nome (str): String que deseja limpar

        Returns:
            str: string formatada
        """
        substitutions = {
            'Ã': 'A', 'Á': 'A', 'À': 'A', 'Â': 'A','Ã':'A', 'Ä': 'A', 'ã': 'a', 'á': 'a', 'à': 'a', 'â': 'a', 'ä': 'a',
            'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E', 'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
            'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I', 'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
            'Õ': 'O', 'Ô': 'O', 'Ó': 'O', 'Ò': 'O', 'Ö': 'O', 'õ': 'o', 'ô': 'o', 'ó': 'o', 'ò': 'o', 'ö': 'o',
            'Ú': 'U', 'Ù': 'U', 'Û': 'U', 'Ü': 'U', 'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
            'Ç': 'C', 'ç': 'c',',':'','/':' '
        }
        for original, replacement in substitutions.items():
            nome = nome.replace(original, replacement)
        return nome
    def corretor_codigo_barra(self,codigo):
        """Método para corrigir 0 a esquerda do código de barras de

        Args:
            codigo (_type_): codigo de barras
        """
        if codigo:
            codigo_barra = str(int(codigo))
            return codigo_barra
        else:
            return codigo
        
    def corrigir_unidade(self,unidade:str) -> str:
        """Converte a unidade em unidade lida pelo AutoSystem

        Args:
            unidade (str): Unidade de medida em string

        Returns:
            str: devolve a sigla do AS
        """
        match unidade:
            case 'AMPERE':
                return 'A'
            case 'AMPERE/HORA':
                return 'AH'
            case 'CENTIMETRO':
                return 'CM'
            case 'CAIXA':
                return 'CX'
            case 'GRAMA':
                return 'G'
            case 'GALAO':
                return 'GL'
            case 'HORA':
                return 'H'
            case 'HERTZ':
                return 'HZ'
            case 'QUILOGRAMA':
                return 'KG'
            case 'KILOGRAMA':
                return 'KG'
            case 'QUILOHERTZ':
                return 'KHZ'
            case 'QUILOVOLT':
                return 'KV'
            case 'QUILOWATT':
                return 'KW'
            case 'LITRO':
                return 'L'
            case 'MILILITRO':
                return 'L'
            case 'METRO':
                return 'M'
            case 'METRO QUADRADO':
                return 'M2'
            case 'METRO CUBICO':
                return 'M3'
            case 'MILIGRAMA':
                return 'MG'
            case 'MEGAHERTZ':
                return 'MHZ'
            case 'MINUTO':
                return 'MIN'
            case 'MILIMETRO':
                return 'MM'
            case 'MEGAWATT':
                return 'MW'
            case 'PEÇA':
                return 'PC'
            case 'PACOTE':
                return 'PCT'
            case 'CONJUNTO':
                return 'PCT'
            case 'PACK':
                return 'PCT'
            case 'FARDO':
                return 'PCT'
            case 'SEGUNDO':
                return 'S'
            case 'TONELADA':
                return 'T'
            case 'UNIDADE':
                return 'UN'
            case 'MILHEIRO':
                return 'UN'
            case 'MAÇO':
                return 'UN'
            case 'FATIA':
                return 'UN'
            case 'TABLETE':
                return 'UN'
            case 'DISPLAY':
                return 'UN'
            case 'GARRAFA':
                return 'UN'
            case 'BANDEJA':
                return 'UN'
            case 'VOLT':
                return 'V'
            case 'WATT':
                return 'W'
            case 'KIT':
                return 'KIT'
            case _:
                return False

    def identificar_kit(self,unidade):
        if unidade == 'KIT':
            return True

    def corrigir_unidade_posto_facil(self,unidade = 7):
        """
        1 -> CX
        2 -> DUZ
        3 -> KG
        4 -> LTS
        5 -> M³
        6 -> MT
        7 -> UN
        """
        match str(unidade):
            case '1': return "CX"
            case '2': return "PCT"
            case '3': return "KG"
            case '4': return "L"
            case '5': return "M3"
            case '6': return "M2"
            case '7': return "UN"
            case _: return "UN"
            
    def corrigir_tributacao_posto_facil(self,tributacao) -> str:
        """
        1 - Produto tributado (000 no postgres)
        2 - sub-tributado (060 no postgres)
        3 - Isenta (040 no postgres)
        4 - Outros (090 no postgres)
        5 - Outros (090 no postgres)
        """
        match str(tributacao):
            case '1': return "000"
            case '2': return "060"
            case '3': return "040"
            case '4': return "090"
            case '5': return "090"
            case _: return "090"
            
    def corrigir_cst_posto_facil(self,cst,tipo:str = 'saida'):
        """CST DE SAIDA
        1 -> 01 OPERAÇÃO TRIBUTÁVEL COM ALÍQUOTA BÁSICA
        2 -> 04 OPERAÇÃO TRIBUTÁVEL MONOFÁSICA - REVENDA A ALÍQUOTA ZERO
        3 -> 05 OPERAÇÃO TRIBUTÁVEL POR SUBSTITUIÇÃO TRIBUTÁRIA
        4 -> 06 OPERAÇÃO TRIBUTÁVEL A ALÍQUOTA ZERO
        5 -> 07 OPERAÇÃO ISENTA DA CONTRIBUIÇÃO
        6 -> 08 OPERAÇÃO SEM INCIDÊNCIA DA CONTRIBUIÇÃO
        7 -> 49 OUTRAS OPERAÇÕES DE SAÍDA
        8 -> 99 OUTRAS OPERAÇÕES
        9 -> 02 OPERAÇÃO TRIBUTÁVEL COM ALÍQUOTA DIFERENCIADA
        
        CST DE ENTRADA
        12 -> 50 OPERAÇÃO COM DIREITO A CRÉDITO
        27 -> 70 OPERAÇÃO DE AQUISIÇÃO SEM DIREITO A CRÉDITO
        28 -> 71 OPERAÇÃO DE AQUISIÇÃO COM ISENÇÃO
        32 -> 75 OPERAÇÃO DE AQUISIÇÃO POR SUBSTIUIÇÃO TRIBUTÁRIA
        33 -> 98 OUTRAS OPERAÇÕES DE ENTRADA
        """
        if tipo.upper() == 'ENTRADA':
            match str(cst):
                case '12': return '50'
                case '27': return '70'
                case '28': return '71'
                case '32': return '75'
                case '33': return '98' 
                case _: return '98'
        elif tipo.upper() == 'SAIDA':
            match cst:
                case '1': return '01'
                case '2': return '04'
                case '3': return '05'
                case '4': return '06'
                case '5': return '07'
                case '6': return '08'
                case '7': return '49'
                case '8': return '99'
                case '9': return '02'
                case _: return '99'
        else:
            match cst:
                case '1': return '01'
                case '2': return '04'
                case '3': return '05'
                case '4': return '06'
                case '5': return '07'
                case '6': return '08'
                case '7': return '49'
                case '8': return '99'
                case '9': return '02' 
                case '12': return '50'
                case '27': return '70'
                case '28': return '71'
                case '32': return '75'
                case '33': return '98'
                case _: return '99'

def corrigir_generico():
    pass
