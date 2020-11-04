import re
from datetime import datetime, timedelta

patterns = {'cpf': r"(\b\d{3}\.\d{3}\.\d{3}\-\d{2}\b|\b\d{11}\b)",
            'rg': r"(\b\d{1,2}.\d{3}.\d{3}-\d{1}\b|\b\d{8}-\d{1}|\b\d{9}\b)",
            'cep': r"(\b\d{5}-\d{3}\b|\b\d{8}\b)",
            'nascimento': r"(\d+\/\d+\/\d+)",
            'nome': r"(\b[A-Z][a-z]+ [A-Z][a-z]+\b)",
            'telefone': r"(\b\d{4,5}-?\d{4}\b)",
            'email': r"/^[a-z0-9.]+@[a-z0-9]+\.[a-z]+\.([a-z]+)?$/i"}

def SearchData(text, data_to_search=None):
    
    if data_to_search is None:
        list_of_regex = patterns.values()
    else:
        list_of_regex = [patterns[d] for d in data_to_search]
    pattern = re.compile(r'|'.join(list_of_regex))
    all_matches = re.finditer(pattern, text)

    return all_matches

def ClassifyData(all_matches, text, data_to_search=None):
    
    patterns = {'cpf': r"(\b\d{3}\.\d{3}\.\d{3}\-\d{2}\b|\b\d{11}\b)",
                'rg': r"(\b\d{1,2}.\d{3}.\d{3}-\d{1}\b|\b\d{8}-\d{1}|\b\d{9}\b)",
                'cep': r"(\b\d{5}-\d{3}\b|\b\d{8}\b)",
                'nascimento': r"(\d+\/\d+\/\d+)",
                'nome': r"(\b[A-Z][a-z]+ [A-Z][a-z]+\b)",
                'telefone': r"(\b\d{4,5}-?\d{4}\b)",
                'email': r"/^[a-z0-9.]+@[a-z0-9]+\.[a-z]+\.([a-z]+)?$/i"}

    if data_to_search is None:
        patterns_keys = list(patterns.keys())
    else:
        patterns_keys = data_to_search
    
    keywords = ['endereço', 'data de nascimento', 'cpf', 'cep', 'rg', 'telefone']
    
    list_of_rules = []
    
    result = {key:0 for key in patterns.keys()}
    
    if all_matches is not None:
        
        for item in all_matches:
            string = item.group(0)
            span = item.span()
            
            matched_string = text[span[0]:span[1]]

            for key, pat in patterns.items():
                
                if re.match(pat, matched_string) is not None:
                    if result[key]<1:
                        result[key] = 1
                    if check_validity(span, key, matched_string, text) is True:
                        if result[key]<2:
                            result[key] = 2

    if any(x == 2 for x in result.values()):
        result["sensitive"] = 2
    elif any(x == 1 for x in result.values()):
        result["sensitive"] = 1
    else:
        result["sensitive"] = 0

    return result


def check_validity(span, key, matched_string, text):

    if key == 'cpf':
        kw = 'cpf'
        if validate_cpf(matched_string) is True or look_keyword(span, text, key) is True:
            return True
    elif key == 'rg':
        if look_keyword(span, text, ['rg', 'identidade']) is True:
            return True
    elif key == 'cep':
        if look_keyword(span, text, ['cep', 'codigo postal', 'c.e.p']):
            return True
    elif key == 'nascimento':
        if look_keyword(span, text, ['data de nascimento', 'nascido', 'nasceu']) and check_nascimento(matched_string):
            return True
    elif key == 'nome':
        if look_keyword(span, text, ['nome']):
            return True
    elif key == 'telefone':
        if look_keyword(span, text, ['telefone', 'tel', 'fone', 'celular']):
            return True
    elif key == 'email':
        if look_keyword(span, text, ['email', 'correio']):
            return True
    else:
        print('key not implemented')
        return False


def look_keyword(span, text, keyword, string_size=50):

    if type(keyword) is not list:
        keyword = list(keyword)

    # TODO tem sentido ou melhor começar com o inicio da string?
    central_pos = int((span[0] + span[1])/2)

    init_pos, fin_pos = define_string_limits(central_pos, string_size, len(text))
    fragment = text[init_pos:fin_pos]

    if any(k.upper() in fragment.upper() for k in keyword):
        return True



def define_string_limits(central_pos, string_size, text_len):

    if central_pos - string_size < 0:
        init_pos = 0
    else:
        init_pos = central_pos - string_size
    if central_pos + string_size > text_len:
        fin_pos = text_len
    else:
        fin_pos = central_pos + string_size

    return init_pos, fin_pos


def validate_cpf(cpf):
    """ Efetua a validação do CPF, tanto formatação quando dígito verificadores.

    Parâmetros:
        cpf (str): CPF a ser validado

    Retorno:
        bool:
            - Falso, quando o CPF não possuir o formato 999.999.999-99;
            - Falso, quando o CPF não possuir 11 caracteres numéricos;
            - Falso, quando os dígitos verificadores forem inválidos;
            - Verdadeiro, caso contrário.

    Exemplos:

    >>> validate('529.982.247-25')
    True
    >>> validate('52998224725')
    False
    >>> validate('111.111.111-11')
    False
    """


    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais:
    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False

    return True




def check_nascimento(date):

    try:
        date = datetime.strptime(date, "%d/%m/%Y")
    except:
        date = datetime.today()
    diff = datetime.today() - date
    if diff.days > 360:
        return True


    """ Efetua a validação do CPF, tanto formatação quando dígito verificadores.

    Parâmetros:
        cpf (str): CPF a ser validado

    Retorno:
        bool:
            - Falso, quando o CPF não possuir o formato 999.999.999-99;
            - Falso, quando o CPF não possuir 11 caracteres numéricos;
            - Falso, quando os dígitos verificadores forem inválidos;
            - Verdadeiro, caso contrário.

    Exemplos:

    >>> validate('529.982.247-25')
    True
    >>> validate('52998224725')
    False
    >>> validate('111.111.111-11')
    False
    """


    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais:
    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False

    return True


def check_rg(rg):
    pass


def check_crea(crea):
    pass


def check_cep(cep):
    pass


def check_tel(telefone):
    pass


def check_nome(nome):
    pass


def check_email(email):
    pass




def format_output(list_of_rules):

    formatted_list_of_rules = []

    if 'nome' in list_of_rules:
        formatted_list_of_rules.append(1)
    else:
        formatted_list_of_rules.append(0)
    if 'cpf' in list_of_rules:
        formatted_list_of_rules.append(1)
    else:
        formatted_list_of_rules.append(0)
    if 'rg' in list_of_rules:
        formatted_list_of_rules.append(1)
    else:
        formatted_list_of_rules.append(0)
    if 'telefone' in list_of_rules:
        formatted_list_of_rules.append(1)
    else:
        formatted_list_of_rules.append(0)
    if 'nascimento' in list_of_rules:
        formatted_list_of_rules.append(1)
    else:
        formatted_list_of_rules.append(0)
    if 'cep' in list_of_rules:
        formatted_list_of_rules.append(1)
    else:
        formatted_list_of_rules.append(0)
        
    if sum(formatted_list_of_rules) > 0:
        formatted_list_of_rules.append(1)
    else:
        formatted_list_of_rules.append(0)
        
    return formatted_list_of_rules
