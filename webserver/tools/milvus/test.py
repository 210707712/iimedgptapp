import asyncio
import re
from tools.milvus.milvus_handler import MilvusManager
from tools.milvus.file_processor import init_model, extract_text_from_pdf, split_text, \
    generate_embeddings, extract_text_from_doc, \
    extract_text_from_txt
import os
from datetime import datetime
from tools.milvus.config import Config

# 初始化 Milvus 和模型
milvus_manager = MilvusManager()
model = init_model()





def safe_file_write(file_path: str, file_content: bytes):
    with open(file_path, "wb") as f:
        f.write(file_content)


def process_file(file, knowledge_id,filename):
    # 创建
    # milvus_manager.create_collection(knowledge_id)

    # _, ext = os.path.splitext(file.filename)
    # now = datetime.now()
    # formatted_now = now.strftime("%Y%m%d_%H%M%S")
    # new_name = formatted_now + ext
    # file_path = os.path.join('./', new_name)
    # milvus_api.logger.debug(f"Processing file: {file.filename}")

    try:
        # text_content = file.read()

        # safe_file_write(file_path, text_content)

        if file.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        elif file.endswith(".doc") or file.endswith(".docx"):
            text = extract_text_from_doc(file)
        elif file.filename.endswith(".txt"):
            text = extract_text_from_txt(file)
        else:
            raise Exception("Unsupported file type")

        text = re.sub(r'\s+', ' ', text)  # 将多个空白符替换为一个空格
        text_chunks = split_text(text, Config.TEXT_CHUNK_SIZE)
        text_chunks_count = len(text_chunks)

        # milvus_api.logger.debug(f"Generated embeddings for {file.filename}. text_chunks_count = {text_chunks_count}")
        embeddings = generate_embeddings(text_chunks, model)
        filled_array = [filename] * len(text_chunks)
        # milvus_api.logger.debug(f"Inserted embeddings into Milvus for {file.filename}.")
        milvus_manager.insert_embeddings(knowledge_id, embeddings, text_chunks, filled_array)

        milvus_manager.create_index(knowledge_id)

    except Exception as e:
        # milvus_api.logger.error(f"Error processing file {file.filename}: {e}")
        print(f'上传文件异常: {e}')  # 实际应用中应使用日志库
        raise e

    return text_chunks_count


# def upload_files():
#     knowledge_id = request.form.get('zhishiid')
#     if 'file' in request.files:
#         file = request.files['file']
#     else:
#         return {"code": 1, "err": 1, "message": "上传文件为空", "data": {}}

#     milvus_manager.create_collection(knowledge_id)
#     total_chunks = process_file(file, knowledge_id)

#     # milvus_api.logger.debug(f"Received {len(files)} files for processing.")

#     # 使用异步编程处理多个文件
#     # tasks = [asyncio.create_task(process_file(file, knowledge_id)) for file in files]
#     # results = await asyncio.gather(*tasks)

#     milvus_manager.create_index(knowledge_id)

#     result = {
#         "code": 20000,
#         "err": 0,
#         "message": "上传成功",
#         "data": {"total_chunks": total_chunks}
#     }
#     return result


def query(query_text,knowledge_id):
    # data = request.json
    # query_text = data.get("query")
    # knowledge_id = request.json['zhishiid']
    if not query_text:
        return {"code": 1, "err": 1, "message": "检索文本为空", "data": {}}
    query_embedding = model.encode(query_text, normalize_embeddings=True).tolist()
    results = milvus_manager.search_query(knowledge_id, query_embedding)
    # print(results)
    response = [{"id": res.entity.get("id"),"text": res.entity.get("text"), "title": res.entity.get("title"),"score": res.distance} for res in results[0]]
    # milvus_api.logger.debug(f"response:{response}")
    result = {
        "code": 20000,
        "err": 0,
        "message": "检索成功",
        "data": {"querytext": response}
    }
    return result
def process_directory(directory_path, knowledge_id):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            print(file)
            file_path = os.path.join(root, file)
            process_file(file_path, knowledge_id,file)
if __name__ == "__main__":
    # milvus_manager.create_index(7880)
    # process_file(file_path,7878)

    # res = query("针刺麻醉、针灸器械", 7879)
    # print(res)

    # file_path=""C:\Users\21070\Desktop\杨比赛\pdfall\中医\(中医)民间妙方.txt""
    # process_file(file_path,7878)



    directory_path = r"Z:\肿瘤\知网论文\心脏"
    knowledge_id = 7880
    process_directory(directory_path, knowledge_id)