"use client";

import axios from "axios";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";


export type EventType = {
  data: string;
  timestamp: string;
};

export type NamedUrl = {
  name: string;
  url: string;
};

export type SearchInfo = {
  topic: string;
  category: string;
  web_urls: string[];
  
};


export const useCrewSearch = () => {
  // State
  const [running, setRunning] = useState<boolean>(false);
  const [topics, setTopics] = useState<string[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [events, setEvents] = useState<EventType[]>([]);
  const [searchInfoList, setSearchInfoList] = useState<SearchInfo[]>([]);
  const [currentSearchId, setCurrentSearchId] = useState<string>("");


  // useEffects
  useEffect(() => {
    let intervalId: number;
    console.log("search crew Id", currentSearchId);

    const fetchSearchStatus = async () => {
      try {
        console.log("calling fetchSearchStatus");
        const response = await axios.get<{
          status: string;
          result: { searchs: SearchInfo[] };
          events: EventType[];
        }>(`http://localhost:3001/api/crew/${currentSearchId}`);
        const { status, events: fetchedEvents, result } = response.data;
        
        console.log("status update", response.data);

        setEvents(fetchedEvents);
        if (result) {
          console.log("setting Search result", result);
          console.log("setting Search categories", result.searchs);
          setSearchInfoList(result.searchs || []);
          
        }
          

        if (status === "COMPLETE" || status === "ERROR") {
          if (intervalId) {
            clearInterval(intervalId);
          }
          setRunning(false);
          toast.success(`Search ${status.toLowerCase()}.`);
        }
      } catch (error) {
        if (intervalId) {
          clearInterval(intervalId);
        }
        setRunning(false);
        toast.error("Failed to get Search status.");
        console.error(error);
      }
    };

    if (currentSearchId !== "") {
      intervalId = setInterval(fetchSearchStatus, 1000) as unknown as number;
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [currentSearchId]);

  const startSearch = async () => {
    // Clear previous Search data
    setEvents([]);
    setSearchInfoList([]);
    setRunning(true);

    try {
      const response = await axios.post<{ search_id: string }>(
        "http://localhost:3001/api/crew",
        {
          topics,
          categories,
        }
      );

      toast.success("Search started");

      console.log("SearchId", response.data.search_id);
      setCurrentSearchId(response.data.search_id);
    } catch (error) {
      toast.error("Failed to start Search");
      console.error(error);
      setCurrentSearchId("");
    }
  };

  return {
    running,
    events,
    setEvents,
    searchInfoList,
    setSearchInfoList,
    currentSearchId,
    setCurrentSearchId,
    topics,
    setTopics,
    categories,
    setCategories,
    startSearch,
   
  };
};

