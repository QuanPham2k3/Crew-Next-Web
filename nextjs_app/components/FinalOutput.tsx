import React from "react";
import { SearchInfo } from "@/hooks/useCrewJob";

interface FinalOutputProps {
  searchInfoList: SearchInfo[];
}

export const FinalOutput: React.FC<FinalOutputProps> = ({searchInfoList,}) => {
  const capitalizeFirstLetter = (string: string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };

  return (
    <div className="flex flex-col h-full">
      <h2 className="text-lg font-semibold my-2">Final Output</h2>
      <div className="flex-grow overflow-auto border-2 border-gray-300 p-2">
        {searchInfoList.length === 0 ? (
          <p>No result yet.</p>
        ) : (
          searchInfoList.map((search, index) => (
            <div key={index} className="mb-4">
              <div className="ml-4">
                <p>
                  <strong>Topic:</strong>{" "}
                  {capitalizeFirstLetter(search.topic)}
                </p>
                <p>
                  <strong>Category:</strong>{" "}
                  {capitalizeFirstLetter(search.category)}
                </p>
                {/* <p>
                  <strong>Name:</strong> {search.name}
                </p> */}
                <div>
                  <strong>Web Articles URLs:</strong>
                  <ul>
                    {search.web_urls.length > 0 ? (
                      search.web_urls.map((url, urlIndex) => (
                        <li key={urlIndex}>
                          <a
                            href={url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-green-500 underline"
                          >
                            {url}
                          </a>
                        </li>
                      ))
                    ) : (
                      <p>None</p>
                    )}
                  </ul>
                </div>         
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
