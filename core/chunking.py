import os
import re
import docx
from typing import List, Dict, Optional
from dataclasses import dataclass
from config.settings import settings

@dataclass
class DocumentChunk:
    content: str
    metadata: Dict
    
class Chunker:
    def __init__(self):
        pass
    
    def load_and_chunk(self) -> List[DocumentChunk]:
        all_chunks = []
        if not os.path.exists(settings.DATA_DIR):
            raise FileNotFoundError(f"Data directory {settings.DATA_DIR} does not exist.")
        
        if os.path.exists(settings.LAWS_DIR):
            print(f"Loading laws from {settings.LAWS_DIR}")
            for filename in os.listdir(settings.LAWS_DIR):
                if filename.endswith(".docx"):
                    file_path = os.path.join(settings.LAWS_DIR, filename)
                    chunks = self._process_law_file(file_path, filename)
                    all_chunks.extend(chunks)
                
                else:
                    print(f"Laws directory not found at {settings.LAWS_DIR}")
                    
            general_docs = [
                (settings.JUDGMENTS_DIR, "judgments"),
                (settings.FATWAS_DIR, "fatwas")
            ]
            
            for dir_path, doc_type in general_docs:
                if os.path.exists(dir_path):
                    print(f"Processing {doc_type} from {dir_path}")
                    for filename in os.listdir(dir_path):
                        if filename.endswith(".docx"):
                            file_path = os.path.join(dir_path, filename)
                            chunks = self._process_general_file(file_path, filename, doc_type)
                            all_chunks.extend(chunks)
                        
                        else:
                            print(f"{doc_type} directory not found at {dir_path} or empty")
                            
        print(f"Total chunks created: {len(all_chunks)}")
        return all_chunks
    
    def _read_docx(self, file_path:str) -> str:
        try:
            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                text = para.text.strip()
                if text:
                    full_text.append(text)
            return "\n".join(full_text)
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return ""
    
    def _process_law_file(self, file_path:str, filename:str) -> List[DocumentChunk]:
        text = self._read_docx(file_path)
        chunks = []
        pattern = re.compile(r'(المادة\s+\d+.*?)(?=\nالمادة|\Z)', re.DOTALL)
        matches = pattern.findall(text)
        
        if not matches:
            return [DocumentChunk(content=text, metadata={"source": filename, "type": "law", "strategy": "fallback"})]
        for match in matches:
            clean_content = match.strip()
            if len(clean_content) > 20:
                chunks.append(DocumentChunk(
                    content=clean_content,
                    metadata={"source": filename, "type": "law", "strategy": "structural_article"}
                ))
        return chunks
    
    def _process_general_file(self, file_path:str, filename:str, doc_type: str) -> List[DocumentChunk]:
        text = self._read_docx(file_path)
        chunks = []
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        current_chunk_text = ""
        limit = settings.CHUNK_SIZE

        for para in paragraphs:
            if len(para) > limit:
                if current_chunk_text:
                    chunks.append(DocumentChunk(
                        content=current_chunk_text.strip(),
                        metadata={"source": filename, "type": doc_type, "strategy": "paragraph_aware"}
                    ))
                    current_chunk_text = ""
                
                chunks.append(DocumentChunk(
                    content = para,
                    metadata={"source": filename, "type": doc_type, "strategy": "large_paragraph"}
                ))
                continue
            
            if len(current_chunk_text) + len(para) > limit:
                chunks.append(DocumentChunk(
                    content=current_chunk_text.strip(),
                    metadata={"source": filename, "type": doc_type, "strategy": "paragraph_aware"}
                ))
                current_chunk_text = para
            else:
                if current_chunk_text:
                    current_chunk_text += "\n" + para
                else:
                    current_chunk_text = para
                    
        if current_chunk_text:
            chunks.append(DocumentChunk(
                content=current_chunk_text.strip(),
                metadata={"source": filename, "type": doc_type, "strategy": "paragraph_aware"}
            ))
            
        return chunks