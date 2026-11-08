import { useSearchParams } from "react-router-dom";

interface PaginationParams
{
    currentPage: number,
    totalPages: number
}

export function Pagination({currentPage, totalPages} : PaginationParams)
{
    const [searchParams, setSearchParams] = useSearchParams();

    function changePage(page: number)
    {
        if(page <= totalPages && page > 0)
        {
            const paramsToUpdate = new URLSearchParams(searchParams);
            paramsToUpdate.set('page', page.toString());
            setSearchParams(paramsToUpdate);
        }
    }

    return(
        <>
            {currentPage <= totalPages && currentPage > 0 &&
            <div className="text-white flex items-center gap-1">
                <button onClick={() => changePage(currentPage - 1)} className="bg-[#1f1f23] text-gray-400 px-2.5 py-1 rounded-2xl hover:cursor-pointer hover:bg-[#2f2f34]">{"< Prev"}</button>
                {
                    currentPage - 3 > 0 &&
                    <>
                        <button onClick={() => changePage(totalPages)} className="px-3 py-1 rounded-4xl hover:cursor-pointer">1</button>
                        <span>...</span>
                    </>
                }
                { currentPage - 2 > 0 &&
                    <>
                        <button onClick={() => changePage(1)} className="px-3 py-1 rounded-4xl hover:cursor-pointer">{currentPage - 2}</button>
                    </>
                }
                { currentPage - 1 !== 0 &&
                    <button onClick={() => changePage(currentPage - 1)} className="px-3 py-1 rounded-4xl hover:cursor-pointer">{currentPage - 1}</button>
                }
                <button onClick={() => changePage(currentPage)} className="active px-3 py-1 rounded-4xl hover:cursor-pointer">{currentPage}</button>
                { currentPage + 1 <= totalPages &&
                    <button onClick={() => changePage(currentPage + 1)} className="px-3 py-1 rounded-4xl hover:cursor-pointer">{currentPage + 1}</button>
                }
                { currentPage + 2 <= totalPages &&
                    <>
                        <button onClick={() => changePage(currentPage + 2)} className="px-3 py-1 rounded-4xl hover:cursor-pointer">{currentPage + 2}</button>
                    </>
                }
                {
                    currentPage + 3 <= totalPages &&
                    <>
                        <span>...</span>
                        <button onClick={() => changePage(totalPages)} className="px-3 py-1 rounded-4xl hover:cursor-pointer">{totalPages}</button>
                    </>
                }
                <button onClick={() => changePage(currentPage + 1)} className="bg-[#1f1f23] text-gray-400 px-2.5 py-1 rounded-2xl hover:cursor-pointer hover:bg-[#2f2f34]">{"Next >"}</button>
            </div>
            }
        </>
    )
}