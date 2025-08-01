import React from "react";
import { Document, Page, pdfjs } from "react-pdf";
import workerSrc from "pdfjs-dist/build/pdf.worker.mjs?url";

pdfjs.GlobalWorkerOptions.workerSrc = workerSrc;

interface ResumePreviewProps {
  file: File | Blob;
}

const ResumePreview: React.FC<ResumePreviewProps> = ({ file }) => {
  return (
    <div>
      <Document file={file}>
        <Page pageNumber={1} />
      </Document>
    </div>
  );
};

export default ResumePreview;
