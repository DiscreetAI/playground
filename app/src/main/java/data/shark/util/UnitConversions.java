package data.shark.util;

import java.text.ParseException;
import java.text.SimpleDateFormat;

/**
 * Created by mujtaba on 5/25/17.
 */

public class UnitConversions {

    private SimpleDateFormat jsonDateFormat;

    private UnitConversions() {
        this.jsonDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSZ");
    }

    public static java.util.Date dateFromJSONString(String string) {
        java.util.Date result = null;
        UnitConversions instance = UnitConversions.getInstance();
        if (string != null) {
            try {
                result = instance.jsonDateFormat.parse(string);
            } catch (ParseException e) {
                e.printStackTrace();
            }
        }
        return result;
    }

    public static String dateToJSONString(java.util.Date date) {
        String result = null;
        UnitConversions instance = UnitConversions.getInstance();
        if (date != null) {
            result = instance.jsonDateFormat.format(date);
        }
        return result;
    }

    public static UnitConversions getInstance() {
        return UnitConversions.UnitConversionsHolder.INSTANCE;
    }

    private static class UnitConversionsHolder {
        private static final UnitConversions INSTANCE = new UnitConversions();
    }

}
