import random
from collections import defaultdict
from konlpy.tag import Okt

def generate_sentence(file_path, order, num_sentences):
    # 문장 생성을 위한 마르코프 체인 초기화
    markov_chain = defaultdict(list) # 기본값을 리스트로 설정
    state_counts = defaultdict(int)  # 기본값을 0으로 설정
    
    
    # 형태소 분석기 초기화
    tokenizer = Okt()

    # 텍스트 파일 읽기
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
   
    # 문장 분리 ['굳 ㅋ', 'GDNTOPCLASSINTHECLUB', '뭐야 이 평점들은.... 나쁘진 않지만 10점 짜리는 더더욱 아니잖아']
    sentences = text.split('\n')
    
    # 마르코프 체인 구성
    for sentence in sentences:
         # 형태소 분석 ['개봉', '되다니', '믿어지지', '않음']
        morphemes = tokenizer.morphs(sentence)
        # 구두점 제거 
        words = [morpheme for morpheme in morphemes if morpheme not in ['!', '?','~',',','.',';']]

        for i in range(len(words) - order): # 현재 단어와 그 뒤에 따르는 단어들을 차수(order)만큼 묶어서 마르코프 체인을 구성하기 위한 루프
           
            prefix = tuple(words[i:i + order])
            
            suffix = words[i + order]
            
             # 차수가 2일때 예 prefix ('개봉', '되다니') suffix 믿어지지  prefix ('되다니', '믿어지지')  suffix 않음
             # {('개봉', '되다니'):[믿어지지, 기뻐요, 실망임]}
            markov_chain[prefix].append(suffix)
            
            
            # {(('개봉', '되다니'),'믿어지지'):1}
            # {(('개봉', '되다니'),'기뻐요'):2}
            # {(('개봉', '되다니'),'실망임'):1}
            state_counts[(prefix, suffix)] += 1
            # print(state_counts)

    generated_sentences = []

    # 문장 생성
    for _ in range(num_sentences):
        current_prefix = random.choice(list(markov_chain.keys())) # 처음 시작 단어 랜덤 선택
        sentence = list(current_prefix)   # 새롭게 생성할 문장 초기화

        while True:
            next_words = markov_chain[current_prefix]
            if not next_words:     #  다음 단어를 예측할 수 없는 경우 문장 생성 중단
                break
            # 빈도에 따른 확률가중치 계산: 
            weights = [state_counts[(current_prefix, suffix)] for suffix in next_words]
            next_word = random.choices(next_words, weights=weights)[0]  # random.choices 함수는 weights라는 확률 가중치로 k개의, 원소를 선택, k를 지정하지 않으면 default로 하나만 선택
            sentence.append(next_word)
            
            if next_word.endswith('.') or next_word.endswith('!') or next_word.endswith('?'):
                break
            # sentence에서 마지막 두개의 단어를 선택하여 tuple로 만듦
            # 생성된 문장이 ["개봉", "되다니", "정말", "기뻐요"]라면 ("정말", "기뻐요") 튜플이 만들어짐.
            current_prefix = tuple(sentence[-order:])  

        generated_sentence = ' '.join(sentence)
        generated_sentences.append(generated_sentence)

    return generated_sentences

file_path = 'text.txt'
order = 2   # 마르코프 체인의 차수, 2 bi-gram, 3 tri-gram
num_sentences = 5

sentences = generate_sentence(file_path, order, num_sentences)

for i, sentence in enumerate(sentences):
    print(f'Sentence {i+1}: {sentence}')