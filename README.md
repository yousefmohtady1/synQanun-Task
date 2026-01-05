# SynQanun Semantic Search

SynQanun is a semantic search engine designed for legal documents. It ingests laws, judgments, and fatwas, processes them into chunks, creates embeddings using `SentenceTransformers`, and stores them in a ChromaDB vector database for fast similarity search.

## Features

- **Document Ingestion**: Supports `.docx` files for Laws, Judgments, and Fatwas.
- **Smart Chunking**: Uses structure-aware chunking for articles and paragraph-aware chunking for general text.
- **Semantic Search**: Powered by `sentence-transformers` and `ChromaDB`.
- **API**: Provides a REST API using `FastAPI` to query the knowledge base.
- **Auto-Pipeline**: Automatically ingests and indexes data on startup if artifacts are missing.

## Chunking Strategy

This project employs a hybrid chunking strategy designed to maximize retrieval relevance for different legal document types:

1.  **Structural Chunking (Laws)**:
    *   **Logic**: Laws are strictly structured by "Articles" (المادة). We use Regex to split the text exactly at article boundaries.
    *   **Reasoning**: Users typically search for specific legal provisions. Splitting by article preserves the complete semantic unit of the law, ensuring that the embedding represents the full legal rule without fragmentation.

2.  **Paragraph-Aware Chunking (Judgments & Fatwas)**:
    *   **Logic**: These are narrative texts. We split by paragraphs but respect a maximum token/character limit (`CHUNK_SIZE`). If a paragraph exceeds the limit, it is recursively split. If it's too small, it is merged with the next one.
    *   **Reasoning**: Narrative context is crucial. Arbitrary fixed-size splitting breaks sentences and meaning. Paragraph-aware chunking maintains semantic coherence while ensuring chunks fit within the embedding model's context window.

## Limitations

1.  **OCR/PDF Support**: Currently supports `.docx` only. PDF/Images require an OCR pipeline (Tesseract/easy ocr) which is out of scope.
2.  **Naive Aggregation**: Document-level relevance is calculated based on the maximum score of its best chunk. This might favor documents with one highly relevant sentence over documents that are moderately relevant throughout.
3.  **Arabic NLP**: Basic normalization is applied. Advanced stemming or lemmatization could improve recall but might degrade precision for specific legal terminologies.

## Project Structure

```
synQanun-Task/
├── app.py                 # FastAPI Application entry point
├── config/               
│   └── settings.py        # Project settings (paths, model names)
├── core/
│   ├── chunking.py        # Document parsing and chunking logic
│   ├── data_pipeline.py   # Orchestrates the ingestion process
│   ├── embeddings.py      # Embedding model wrapper
│   ├── main_pipeline.py   # Search service wrapper
│   └── vector_store.py    # ChromaDB vector store management
└── data/                  # Place your .docx files here
    ├── laws/
    ├── judgments/
    └── fatwas/
```

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd synQanun-Task
    ```

2.  **Install Dependencies**:
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

    *Note: Initializes `sentence-transformers` which might download the model (`intfloat/multilingual-e5-large`) on first run.*

## Usage

### 1. Prepare Data
Place your Word documents (`.docx`) in the appropriate folders under `data/`:
- `data/laws/`
- `data/judgments/`
- `data/fatwas/`

### 2. Run the Application
Start the API server:
```bash
python app.py
```
*Or directly with uvicorn:*
```bash
uvicorn app:app --reload
```

On the first run, the system will detect missing artifacts and run the ingestion pipeline automatically:
1.  Load and chunk documents.
2.  Generate embeddings.
3.  Store them in the ChromaDB collection.

### 3. API Documentation
Once running, access the automatic API docs at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Example Output
Endpoint: POST /search Query: "هل يجوز الجمع بين المرتب والمعاش أو المكافأة؟" (Is it permissible to combine salary with pension or bonus?)

```json
{
  "query": "ما هو أثر وجود فاصل زمني عند إعادة تعيين العامل بالنسبة لأجره؟",
  "count": 2,
  "results": [
    {
      "source": "fatwa2_1990.docx",
      "doc_type": "fatwas",
      "max_score": 0.6027466058731079,
      "chunks": [
        {
          "content": "والمستفاد من ذلك أن الأصل العام فى تحديد المعاملة المالية للعاملين أن يحصل العامل عند تعينيه على بداية الأجر المقرر لدرجة الوظيفة المعين عليها، واستثناء من هذا الأصل احتفظ المشرع للعامل الذى يعاد تعينيه فى وظيفة من مجموعة أخرى فى نفس درجته أو فى درجة أخرى بالأجر الذى كان يتقاضاه فى وظيفته السابقة إذا كان أجره فى الوظيفة السابقة أكبر من الأجر المقرر للوظيفة المعين عليها، على ألا يجاوز نهايته. واشترط لذلك أن تكون مدة الخدمة متصلة بحيث لا يقطع اتصالها أى فاصل زمنى أياً كانت مدته. فإذا توافر مناط هذا الإحتفاظ وهو اتصال مدة الخدمة احتفظ العامل الذى يعاد تعينيه بأجره فى الوظيفة السابقة أما إذا تخلف هذا المناط وجب تحديد المعاملة المالية للعامل فى الوظيفة الجديدة على أساس بداية مربوط الدرجة المعين عليها.\nالرأى\nومن حيث إنه لما كان ذلك، وكان الثابت من الأوراق أن السيد اللواء/... أحيل إلى المعاش فى 1/7/1985 وكان مرتبه الأساسى 202.750 مليم وجنيه ثم أعيد تعيينه فى وظيفة رئيس إدارة مركزية من الدرجة العالية بوزارة الطيران المدنى فى 10/3/1986 وبداية مربوطها 140.000 مليم جنيه وأن السيد اللواء/... أحيل إلى المعاش فى أول يونيه سنة 1981 وكان مرتبه الأساسى 202.750 ثم أعيد تعيينه فى وظيفة من الدرجة العالية بوزارة الطيران المدنى فى 12/5/1987 وبداية مربوطها 140.000 مليم جنيه لما كان ذلك فإن الاستثناء الذى أورده نص المادة (25) من القانون رقم (47) لسنة 1978 المشار إليه لإحتفاظ العامل بمرتبه فى الوظيفة السابقة عند تعيينه فى الوظيفة الجديدة لا يجوز تطبيقه فى شأن السيدين المذكورين لوجود فاصل زمنى بين الإحالة إلى المعاش فى القوات المسلحة، وإعادة التعيين فى وزارة الطيران المدنى. وتبعا لذلك فإن المرتب المستحق لكل منهما عند إعادة التعيين يتحدد على أساس بداية درجة الوظيفة التى أعيد التعيين عليها وهو 140.000 مليم جنيه.",
          "score": 0.6027466058731079,
          "metadata": {
            "source": "fatwa2_1990.docx",
            "strategy": "paragraph_aware",
            "type": "fatwas"
          }
        },
        {
          "content": "جمهورية مصر العربية - الفتوى رقم 87 لسنة 1990 بتاريخ 1990-01-18 تاريخ الجلسة 1989-12-20\nمبدأ 1\nعاملون مدنيون بالدولة ـ تعيين ـ إعادة تعيين\nالمادة (25) من قانون العاملين المدنيين بالدولة رقم (47) لسنة 1978 ـ الأصل العام فى تحديد المعاملة المالية للعاملين أن يحصل العامل عند تعيينه على بداية الأجر المقرر لدرجة الوظيفة المعين عليها ـ استثناءاً من هذا الأصل احتفظ المشرع للعامل الذى يعاد تعيينه فى وظيفة من مجموعة أخرى فى نفس درجته أو فى درجة أخرى بالأجر الذى كان يتقاضاه فى وظيفته السابقة إذا كان أجره فى الوظيفة السابقة أكبر من الأجر المقرر للوظيفة المعين عليها على أن لا يجاوز نهايته ـ مناط هذا الإحتفاظ ـ أن تكون مدة الخدمة متصلة بحيث لا يقطع اتصالها أى فاصل زمنى أياً كانت مدته ـ أثر ذلك ـ إذا تخلف هذا المناط وجب تحديد المعاملة المالية للعامل فى الوظيفة الجديدة على أساس بداية مربوط الدرجة المعين عليها ـ تطبيق.\nتنص المادة (25) من قانون نظام العاملين المدنيين بالدولة الصادر بالقانون رقم (47) لسنة 1978 على أن يستحق العامل عند التعيين بداية الأجر المقرر لدرجة الوظيفة طبقاً لجدول الأجور رقم (1) المرافق لهذا القانون.\nويستحق العامل أجره إعتباراً من تاريخ تسلمه العمل، ما لم يكن مستبقى بالقوات المسلحة فيستحق أجره من تاريخ تعيينه واستثناء من ذلك إذا أعيد تعيين العامل فى وظيفة من مجموعة أخرى فى نفس درجته أو فى درجة أخرى احتفظ له بالأجر الذى كان يتقاضاه فى وظيفته السابقة إذا كان يزيد على بداية الأجر المقرر للوظيفة المعين عليها بشرط إلا يجاوز نهايته وأن تكون مدة خدمته متصلة.\nويسرى هذا الحكم على العاملين السابقين بالوحدات الاقتصادية والمعاملين بنظم خاصة الذين يعاد تعينيهم فى الوحدات التى تسرى عليها أحكام هذا القانون.",
          "score": 0.5669423341751099,
          "metadata": {
            "type": "fatwas",
            "source": "fatwa2_1990.docx",
            "strategy": "paragraph_aware"
          }
        }
      ]
    },
    {
      "source": "قانون - رقم 6.docx",
      "doc_type": "law",
      "max_score": 0.49117493629455566,
      "chunks": [
        {
          "content": "المادة 44\nتحصل الجهة الإدارية مقابل تأخير عن المبالغ التي تورد بعد الموعد المحدد لها وعن باقي السلفة المؤقتة التي تتأخر تسويتها عن المواعيد المقررة، ويراعى في تقدير ذلك المقابل أن يكون محسوبا على أساس سعر الإقراض والخصم الساري المعلن من البنك المركزي في التاريخ المحدد للتوريد أو تسوية السلفة أيهما أعلى، وذلك ما لم تقض قوانين أخرى بفرض مقابل أعلى.\nويساءل المتسببون من القائمين على التحصيل أو أصحاب السلف عن التأخير في توريد المبالغ المحصلة أو تسوية السلفة، وفقا لقانون الخدمة المدنية أو القانون أو القرار المنظم لشئون الجهة.\nوللوزير تخفيض المقابل المشار إليه أو الإعفاء منه، إذا ثبت أن التأخير كان لعذر قهري، وتوضح اللائحة التنفيذية القواعد والإجراءات المنظمة لذلك.\nمادة 45",
          "score": 0.49117493629455566,
          "metadata": {
            "source": "قانون - رقم 6.docx",
            "type": "law",
            "strategy": "structural_article"
          }
        }
      ]
    }
  ]
}
```