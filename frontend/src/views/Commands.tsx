export function Commands()
{
    const mocked_elements: string[] = ["element 1", "element 2", "element 3"]

    return(
        <>
            {/* Container */}
            <div className="flex h-screen">
                {/* Create command */}
                <div className="flex-1 bg-gray-200 mx-3 my-5 rounded-2xl"></div>
                {/* Command list */}
                <div className="flex-1 bg-blue-300 mx-3 my-5 rounded-2xl">
                    <div className="bg-green-100 rounded-2xl mb-3">
                        <input type="text" className="border border-gray-500 bg-white text-black rounded-md p-3 m-3"></input>
                    </div>
                    {mocked_elements.map((element) => (
                        <>
                            <div className="bg-red-100 p-3 rounded-2xl mb-1">
                                {element}
                            </div>
                        </>
                    ))}
                </div>
            </div>
        </>
    )
}