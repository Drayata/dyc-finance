'use client';

import React, { useEffect, useRef, useState } from 'react';
import { createChart, ColorType, IChartApi, ISeriesApi, Time } from 'lightweight-charts';

export interface CandleData {
  time: string | number; // String 'YYYY-MM-DD' or timestamp
  open: number;
  high: number;
  low: number;
  close: number;
}

interface CandlestickChartProps {
  data: CandleData[];
  width?: number;
  height?: number;
}

export default function CandlestickChart({ data, width, height = 400 }: CandlestickChartProps) {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<"Candlestick"> | null>(null);
  const [isDarkMode, setIsDarkMode] = useState(true);

  // Detect theme (very basic implementation for MVP)
  useEffect(() => {
    const isDark = document.documentElement.classList.contains('dark') || 
                   window.matchMedia('(prefers-color-scheme: dark)').matches;
    setIsDarkMode(isDark);
  }, []);

  useEffect(() => {
    if (!chartContainerRef.current) return;

    const handleResize = () => {
      if (chartRef.current && chartContainerRef.current) {
        chartRef.current.applyOptions({ 
          width: chartContainerRef.current.clientWidth 
        });
      }
    };

    const textColor = isDarkMode ? '#A3A3A3' : '#525252';
    const gridColor = isDarkMode ? '#262626' : '#e5e5e5';
    const bgColor = isDarkMode ? 'transparent' : 'transparent';

    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: bgColor },
        textColor,
        fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
      },
      grid: {
        vertLines: { color: gridColor },
        horzLines: { color: gridColor },
      },
      width: chartContainerRef.current.clientWidth,
      height,
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
        borderColor: gridColor,
      },
      rightPriceScale: {
        borderColor: gridColor,
      }
    });

    chartRef.current = chart;

    // @ts-ignore - type definition in v4
    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#10b981',      // var(--bullish)
      downColor: '#ef4444',    // var(--bearish)
      borderVisible: false,
      wickUpColor: '#10b981',
      wickDownColor: '#ef4444',
    });
    
    seriesRef.current = candlestickSeries;

    // Formatting data for lightweight-charts (requires time as YYYY-MM-DD or unix timestamp)
    const formattedData = data.map(d => {
      // If time is ISO string, convert to YYYY-MM-DD
      let timeVal = d.time;
      if (typeof timeVal === 'string' && timeVal.includes('T')) {
        timeVal = timeVal.split('T')[0];
      }
      return {
        ...d,
        time: timeVal as Time
      };
    });
    
    // Ensure data is sorted by time
    formattedData.sort((a, b) => {
      if (a.time < b.time) return -1;
      if (a.time > b.time) return 1;
      return 0;
    });

    candlestickSeries.setData(formattedData);
    chart.timeScale().fitContent();

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [data, height, isDarkMode]);

  return (
    <div className="w-full relative">
      <div ref={chartContainerRef} className="w-full" />
    </div>
  );
}
