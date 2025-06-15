# a very rudimentary text to morse code translator, works with letters, puncutation and numbers

def morse_to_txt(morse : str = '') -> str:

    try:
        morse = input('Enter morse code: ')
    except ValueError:
        print('Please enter something')
        morse_to_txt()
    
    code_list = {'alpha' : ['.-', '-...', '.-.-', '-..', '.', '..-.', '--.', '....', '..', '.---', '-.-', '.-..', '--', '-.', '---', '.--.', '--.-', '.-.', '...', '-', '..-', '...-', '.--', '-..-', '-.--', '--..'],
                 'punct' : ['.-.-.-', '--..--', '..--..', '-...-', '-..-.', '.-...', '-.--.', '-.--.-', '.-.-.', '-....-', '-.-.--', '..--.-', '---...', '-.-.-.', '...-..-', '.--.-.', '.----.'],
                 'num' : ['-----', '.----', '..---', '...--', '....-', '.....', '-....', '--...', '---..', '----.']}

    temp =  morse.split('/') if ('/' in morse) else [morse]
    coded_words = [i.strip() for i in temp]  
    coded_letters = [i.split(' ') for i in coded_words]
    final = []
    
    for i in coded_letters:
        word = ''
        for idx in range(len(i)):
            if len(i[idx]) <= 4:
                x = code_list['alpha'].index(i[idx])
                i[idx] = chr(65+x)
            else:
                if i[idx] in code_list['num']:
                    x = code_list['num'].index(i[idx])
                    i[idx] = f'{x}'
                else:
                    x = code_list['punct'].index(i[idx])
            word += i[idx]
        final.append(word)

    uncoded = ''
    for i in final: uncoded += f'{i} '

    print(uncoded)
    morse_to_txt()

if __name__ == "__main__":
    morse_to_txt()
