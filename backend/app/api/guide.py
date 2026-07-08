from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import traceback

from app.schemas.request import GuideRequest
from app.services.guide_service import GuideService


router = APIRouter(
    prefix="/guide",
    tags=["Career Guide"]
)


GENERATED_GUIDES_DIR = Path("generated_guides")


@router.post("/generate")
def generate_guide(request: GuideRequest):

    print("\n================ NEW REQUEST ================")
    print("Question :", request.question)
    print("Model    :", request.model)
    print(
        "API Key  :",
        request.api_key[:10] + "..." if request.api_key else "None"
    )
    print("=============================================\n")


    try:

        graph_result = GuideService.generate(
            question=request.question,
            api_key=request.api_key,
            model=request.model,
        )


        print("\n========== GRAPH RESULT ==========")
        print(graph_result)
        print("==================================\n")


        if isinstance(graph_result, dict):

            if not graph_result.get("continue_pipeline", True):

                return {
                    "status": "stopped",
                    "response": graph_result.get("response"),
                }


            # -------------------------------
            # Final Markdown Response
            # -------------------------------

            final_markdown = (
                graph_result.get("merge_response")
                or graph_result.get("response")
            )


            # Fallback stitching
            if not final_markdown:

                sections = [
                    graph_result.get("intro_response"),
                    graph_result.get("rm_response"),
                    graph_result.get("rcs_response"),
                    graph_result.get("pj_response"),
                    graph_result.get("iv_response"),
                ]

                sections = [
                    section 
                    for section in sections 
                    if section
                ]

                final_markdown = "\n\n---\n\n".join(sections)



            # -------------------------------
            # PDF filename cleanup
            # -------------------------------

            pdf_filename = None

            pdf_path = graph_result.get("pdf_path")


            if pdf_path:

                pdf_filename = Path(pdf_path).name



            return {

                "status": "success",

                "role": graph_result.get("role"),

                "response": final_markdown,

                # only filename returned
                # example:
                # DevOps_Engineer_Career_Guide.pdf
                "pdf_path": pdf_filename,
            }



        return {

            "status": "success",

            "response": graph_result,

        }



    except Exception as e:


        print("\n\n=========== FULL TRACEBACK ===========")

        traceback.print_exc()

        print("======================================\n")


        return {

            "status": "failed",

            "error_type": type(e).__name__,

            "message": str(e),

        }





# =====================================================
# PDF DOWNLOAD
# =====================================================

@router.get("/download/{filename:path}")
def download_pdf(filename: str):


    file_path = GENERATED_GUIDES_DIR / filename


    print("\nPDF DOWNLOAD REQUEST")
    print("Requested:", filename)
    print("Resolved :", file_path)
    print("--------------------")


    if not file_path.exists():

        raise HTTPException(

            status_code=404,

            detail=f"PDF not found: {file_path}"

        )


    return FileResponse(

        path=str(file_path),

        media_type="application/pdf",

        filename=file_path.name,

    )