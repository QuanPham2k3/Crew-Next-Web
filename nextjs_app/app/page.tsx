"use client";

import { EventLog } from "@/components/EventLog";
import { FinalOutput } from "@/components/FinalOutput";
import InputSection from "@/components/InputSection";
import { useCrewSearch } from "@/hooks/useCrewJob";
import {ChatInput} from "@/components/ChatInput";


export default function Home() {
  // Hooks
  const crewSearch = useCrewSearch();

  return (
    <div className="bg-white min-h-screen text-black">
      <div className="flex">
        <div className="w-1/2 p-4">
          <InputSection
            title="Topics"
            placeholder="Add a topic"
            data={crewSearch.topics}
            setData={crewSearch.setTopics}
          />
          <InputSection
            title="Categories"
            placeholder="Add a category"
            data={crewSearch.categories}
            setData={crewSearch.setCategories}
          />
        </div>

        <div className="w-1/2 p-4 flex flex-col">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold">Output</h2>
            <button
              onClick={() => crewSearch.startSearch()}
              className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded text-sm"
              disabled={crewSearch.running}
            >
              {crewSearch.running ? "Running..." : "Start"}
            </button>
          </div>
          <FinalOutput searchInfoList={crewSearch.searchInfoList} />
          <EventLog events={crewSearch.events} />
        </div> 
      </div>
      <div className="w p-4 flex flex-col">
        <ChatInput Search_id={crewSearch.currentSearchId}/>
      </div>
    </div>
  );
}
