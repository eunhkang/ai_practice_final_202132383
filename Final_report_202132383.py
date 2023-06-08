import pandas as pd

class L_ChatBot:                                    # 레벤슈타인기반 챗봇 클래스 정의
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)         # 인스턴스 생성 시 챗봇데이터 불러오기 및 질문&답변 리스트 생성

    # 챗봇 데이터 불러오기 및 질문리스트/답변리스트 생성
    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()              
        answers = data['A'].tolist()                
        return questions, answers

    # 레벤슈타인 거리 (distance) 리스트 구하기 - 챗봇데이터의 모든 질문에 대해 각각 거리를 구해서 리스트로 만들어 반환한다.
    # 사용자 질문 (input_sentence)과 비교할 질문리스트 (questions) 를 입력값으로 받음 
    def calc_distance(self, input_sentence, questions):         
        dist = []                                   # input과 질문 리스트 간 거리를 저장할 리스트 생성
        x_len = len(input_sentence)                 # matrix의 x축: input 문장  
        for question in questions:                  
            y_len = len(question)                   # matrix의 y축: 질문리스트 문장 
            
            # 0으로 초기화 된 matrix 생성           
            matrix = [[] for i in range(y_len+1)]
            for i in range(y_len+1):                
                matrix[i] = [0 for j in range(x_len+1)]
                
            # 첫 행 / 열을 각각 0,1,2,3,..으로 초기화 
            for i in range(y_len+1):
                matrix[i][0] = i
            for j in range(x_len+1):
                matrix[0][j] = j
            
            # 표 채우기
            for i in range(1, y_len+1):
                y_C = question[i-1]
                
                for j in range(1, x_len+1):
                    x_C = input_sentence[j-1] 
                    cost = 0 if (x_C == y_C) else 1
                    change = matrix[i-1][j-1] + cost
                    add = matrix[i][j-1] + 1
                    delete = matrix[i-1][j] + 1
                    matrix[i][j] = min([change, add, delete]) 
                    
            # 표 완성 후 dist에 matrix 마지막 숫자를 추가함        
            dist.append(matrix[y_len][x_len])       
            
        return dist                 
    
    # 최소 거리 인덱스 및 베스트 답변 구하기    
    def find_best_answer(self, input_sentence):
        distance = self.calc_distance(input_sentence, self.questions)       # input에 대한 questions 목록의 distance 리스트 생성
        best_question_idx = distance.index(min(distance))                   # 레벤슈타인 거리 최소값의 인덱스 추출
        best_answer = self.answers[best_question_idx]                       # 답변열 리스트에 인덱스 넣어서 답변 추출
        return best_answer
    
    # 최소 레벤슈타인 거리, 원 데이터에서의 인덱스 및 가장 유사한 질문 확인용 함수
    def detail_check(self, input_sentence):
        t1=self.calc_distance(input_sentence, self.questions)               # t1: input에 대한 dist list
        t2=min(t1)                                                          # t2: 최소 거리

        t3=[]                                                               # t3: 최소 거리 문장의 인덱스. 두 개 이상 발견될 경우를 상정해 리스트로 얻는다.
        for i in range(len(t1)):
            if t1[i] == t2:
                t3.append(i)

        print("최소 레벤슈타인 거리:", t2)
        print("챗봇데이터 인덱스:", t3)                                      
    
        for i in range(len(t3)):                                            # 최소 거리 문장이 여러 개 존재할 경우 input과 유사한 모든 질문 및 그에 해당하는 답변 확인
            print("챗봇데이터 질문:", chatbot.questions[t3[i]])
            print("챗봇데이터 대답:", chatbot.answers[t3[i]])
            

''' 챗봇 생성  '''            
# CSV 파일 경로 지정
filepath = 'ChatbotData.csv'

# 챗봇 인스턴스 생성 - 경로 직접 입력
chatbot = L_ChatBot(filepath)

''' 선택 1. '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복할 경우 아래 코드 활성화 '''
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)

''' 선택 2. 입력한 input과 유사한 오리지널 질문 확인용 코드. 질문이 여러개 검색되는 경우를 확인하기 위해 사용 '''
# input_sentence = input('You: ')                               # 다답변 예시 문장: 술 많이 마시면 건강에 좋지 않아 -> 최소 거리가 11인 10 개의 질문/답변 검색 됨
# response = chatbot.detail_check(input_sentence)