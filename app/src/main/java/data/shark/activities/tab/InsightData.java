package data.shark.activities.tab;

import android.content.Context;
import android.graphics.Paint;
import android.support.v4.content.ContextCompat;

import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;
import com.jjoe64.graphview.series.PointsGraphSeries;

import data.shark.R;

public class InsightData {

    private String insight = "Time to start making money!";
    private PointsGraphSeries<DataPoint> scatterPlot;
    private LineGraphSeries<DataPoint> trendLine;

    public InsightData(String insight, PointsGraphSeries<DataPoint> scatterPlot,
                       LineGraphSeries<DataPoint> trendLine) {
        this.insight = insight;
        this.scatterPlot = scatterPlot;
        this.trendLine = trendLine;
    }

    void customizeSeries(Context context) {
        Paint lineColor = new Paint();
        lineColor.setColor(ContextCompat.getColor(context, R.color.gold));
        lineColor.setStrokeWidth(8f);
        trendLine.setCustomPaint(lineColor);

        scatterPlot.setSize(10f);
        scatterPlot.setColor(R.color.lightBlue);
    }

    String getInsight() {
        return insight;
    }

    PointsGraphSeries<DataPoint> getScatterPlot() {
        return scatterPlot;
    }

    LineGraphSeries<DataPoint> getTrendLine() {
        return trendLine;
    }
}
