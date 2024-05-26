# AUTHOR:   SANDER BETZ
# ST-NR:    6070000
# ST-MAIL:  S.H.R.Betz@student.tudelft.nl

K_1_encrypted = ('EMUFPHZLRFAXYUSDJKZLDKRNSHGNFIVJ '
                 'YQTQUXQBQVYUVLLTREVJYQTMKYRDMFD')

K_2_encrypted = ('VFPJUDEEHZWETZYVGWHKKQETGFQJNCE '
                 'GGWHKK?DQMCPFQZDQMMIAGPFXHQRLG '
                 'TIMVMZJANQLVKQEDAGDVFRPJUNGEUNA '
                 'QZGZLECGYUXUEENJTBJLBQCRTBJDFHRR '
                 'YIZETKZEMVDUFKSJHKFWHKUWQLSZFTI '
                 'HHDDDUVH?DWKBFUFPWNTDFIYCUQZERE '
                 'EVLDKFEZMOQQJLTTUGSYQPFEUNLAVIDX '
                 'FLGGTEZ?FKZBSFDQVGOGIPUFXHHDRKF '
                 'FHQNTGPUAECNUVPDJMQCLQUMUNEDFQ '
                 'ELZZVRRGKFFVOEEXBDMVPNFQXEZLGRE '
                 'DNQFMPNZGLFLPMRJQYALMGNUVPDXVKP '
                 'DQUMEBEDMHDAFMJGZNUPLGEWJLLAETG')

K_3_encrypted = ('ENDYAHROHNLSRHEOCPTEOIBIDYSHNAIA '
                 'CHTNREYULDSLLSLLNOHSNOSMRWXMNE '
                 'TPRNGATIHNRARPESLNNELEBLPIIACAE '
                 'WMTWNDITEENRAHCTENEUDRETNHAEOE '
                 'TFOLSEDTIWENHAEIOYTEYQHEENCTAYCR '
                 'EIFTBRSPAMHHEWENATAMATEGYEERLB '
                 'TEEFOASFIOTUETUAEOTOARMAEERTNRTI '
                 'BSEDDNIAAHTTMSTEWPIEROAGRIEWFEB '
                 'AECTDDHILCEIHSITEGOEAOSDDRYDLORIT '
                 'RKLMLEHAGTDHARDPNEOHMGFMFEUHE '
                 'ECDMRIPFEIMEHNLSSTTRTVDOHW?')

K_4_encrypted = ('OBKR '
                 'UOXOGHULBSOLIFBBWFLRVQQPRNGKSSO '
                 'TWTQSJQSSEKZZWATJKLUDIAWINFBNYP '
                 'VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR')

def viginere_cypher(key: str, text):
    alphabet = ('A B C D E F G H I J K L M N O P Q R S T U V W X Y Z').split(' ')

    cypher = {' ': alphabet}
    for i in range(26):
        lst = []
        for j in range(len(alphabet) + len(key)):
            if j < len(key):
                lst.append(key[j])
            else:
                if alphabet[j - len(key)] in key:
                    continue
                else:
                    lst.append(alphabet[j - len(key)])
        cypher[alphabet[i]] = lst

    for char, item in cypher.items():
        print(char, item)

viginere_cypher('KRYPTOS', K_1_encrypted)











