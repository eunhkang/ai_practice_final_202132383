import pandas as pd

class L_ChatBot:                                    # 레벤슈타인기반 챗봇 클래스 정의
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()              # 질문열 리스트
        answers = data['A'].tolist()                # 답변열 리스트
        return questions, answers

    # 레벤슈타인 거리 리스트 구하기
    def calc_distance(self, input_sentence, questions):        
        dist = []                                   # input과 질문 리스트 간 거리를 저장할 리스트 생성
        x_len = len(input_sentence)                 
        for question in questions:
            y_len = len(question)
            
            if input_sentence == question: 
                dist.append(0)                      # 질문열 중 input과 동일한 문장이 있는 경우 거리: 0
                break
        
            # 0으로 초기화 된 ndarray 생성 / input을 x축, 질문열의 질문을 y축으로 배치           
            matrix = [[] for i in range(y_len+1)]
            for i in range(y_len+1):                # 0으로 초기화
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
            dist.append(matrix[y_len][x_len])       # dist에 매트릭스 마지막 숫자를 추가함
            
        return dist
    # 최소 거리 인덱스 및 베스트 답변 구하기    
    def find_best_answer(self, input_sentence):
        distance = self.calc_distance(input_sentence, self.questions)       # input에 대한 questions 목록의 distance 리스트 생성
        best_question_idx = distance.index(min(distance))                   # 최소 거리의 인덱스 추출
        best_answer = self.answers[best_question_idx]                       # 답변열 리스트에 인덱스 넣어서 답변 추출
        return best_answer
        
# CSV 파일 경로 지정
# filepath = 'ChatbotData.csv'

# 챗봇 인스턴스 생성 - 경로 직접 입력
chatbot = L_ChatBot('ChatbotData.csv')

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)

'''최소 레벤슈타인 거리, 원 데이터에서의 인덱스 및 가장 유사한 질문 확인용 코드'''
# input_sentence = input('You:')
# t1=chatbot.calc_distance(input_sentence, chatbot.questions)
# t2=min(t1)
# t3=t1.index(min(t1))

# # print("t1:", t1)
# print("최소 레벤슈타인 거리:", t2)
# print("챗봇데이터 인덱스:", t3)
# print("챗봇데이터 질문:", chatbot.questions[t3])
# print("챗봇데이터 대답:", chatbot.answers[t3])