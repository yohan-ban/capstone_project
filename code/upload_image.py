def UPLOAD_IMAGE(num, file_path):
    from google.cloud import storage
    import os
    
    #환경변수 세팅
    KEY_PATH = "/home/student/Desktop/project/Project/do-not-clean-f0389649cc6e.json" #다운받은 json 절대 경로

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= KEY_PATH

    ### 인증 확인
    storage_client = storage.Client()
    buckets = list(storage_client.list_buckets())

    #print(buckets) # 결과 => [<Bucket: 버킷 이름>]

    ### GCP에 파일 올리기

    # 관련 참고 링크 : https://soundprovider.tistory.com/entry/GCP-Python%EC%97%90%EC%84%9C-GCP-Cloud-Storage-%EC%97%B0%EB%8F%99%ED%95%98%EA%B8%B0

    # 서비스 계정 생성한 bucket 이름 입력
    bucket_name = 'detected_ob'    
    # GCP에 업로드할 파일 절대경로, 경로 사이 역슬래쉬는 슬래쉬로 변환할 것
    source_file_name = file_path
    # 업로드할 파일을 GCP에 저장할 때의 이름. 새로운 이미지를 넣을 때마다 바꾸어줘야 함
    destination_blob_name = f'Detected{num}'

    # 이미지 업로드하기
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print("upload done!") # 삽입 완료 시 출력 문구