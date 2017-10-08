package data.shark.util;

import android.app.Activity;
import android.content.res.Resources;
import android.graphics.Paint;
import android.util.Log;
import android.util.TypedValue;
import android.view.View;
import android.widget.DatePicker;
import android.widget.TextView;

import java.lang.reflect.Field;

public class DatePickerUtil {

    public static void setFont(View view, DatePicker datepicker, FontUtilities fontUtilities) {
        try {
            Field delegateField = datepicker.getClass().getDeclaredField(
                    "mDelegate");
            delegateField.setAccessible(true);
            Object delegate = delegateField.get(datepicker);

            Field field = delegate.getClass().getDeclaredField("mDaySpinner");
            setFont(view, delegate, field, fontUtilities);
            field = delegate.getClass().getDeclaredField("mMonthSpinner");
            setFont(view, delegate, field, fontUtilities);
            field = delegate.getClass().getDeclaredField("mYearSpinner");
            setFont(view, delegate, field, fontUtilities);
            setFont(view, delegate,
                    delegate.getClass().getDeclaredField("mDaySpinnerInput"), fontUtilities);
            setFont(view, delegate,
                    delegate.getClass().getDeclaredField("mMonthSpinnerInput"), fontUtilities);
            setFont(view, delegate,
                    delegate.getClass().getDeclaredField("mYearSpinnerInput"), fontUtilities);

        } catch (Exception e) {
            Log.e("ERROR", e.getMessage());
        }
    }

    private static void setFont(View view, Object datepicker, Field field, FontUtilities fontUtilities)
            throws Exception {
        field.setAccessible(true);
        Object yearPicker = field.get(datepicker);
        ((View) yearPicker).setVisibility(View.VISIBLE);

        View childpicker = view.findViewById(Resources.getSystem().getIdentifier(
                "month", "id", "android"));
        Field field1 = childpicker.getClass().getDeclaredField("mInputText");
        field1.setAccessible(true);
        Object edittext = field1.get(yearPicker);

        Field field2 = childpicker.getClass().getDeclaredField(
                "mSelectorWheelPaint");
        field2.setAccessible(true);
        Object paint = field2.get(yearPicker);
        ((Paint) paint).setTypeface(fontUtilities.scandiaMedium);

        ((TextView) edittext).setTypeface(fontUtilities.scandiaMedium);
        ((TextView) edittext).setLineSpacing(TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP,
                5.0f, Resources.getSystem().getDisplayMetrics()), 1.0f);
    }

    public static void setFont(Activity activity, DatePicker datepicker, FontUtilities fontUtilities) {
        try {
            Field delegateField = datepicker.getClass().getDeclaredField(
                    "mDelegate");
            delegateField.setAccessible(true);
            Object delegate = delegateField.get(datepicker);

            Field field = delegate.getClass().getDeclaredField("mDaySpinner");
            setFont(activity, delegate, field, fontUtilities);
            field = delegate.getClass().getDeclaredField("mMonthSpinner");
            setFont(activity, delegate, field, fontUtilities);
            field = delegate.getClass().getDeclaredField("mYearSpinner");
            setFont(activity, delegate, field, fontUtilities);
            setFont(activity, delegate,
                    delegate.getClass().getDeclaredField("mDaySpinnerInput"), fontUtilities);
            setFont(activity, delegate,
                    delegate.getClass().getDeclaredField("mMonthSpinnerInput"), fontUtilities);
            setFont(activity, delegate,
                    delegate.getClass().getDeclaredField("mYearSpinnerInput"), fontUtilities);

        } catch (Exception e) {
            Log.e("ERROR", e.getMessage());
        }
    }

    private static void setFont(Activity activity, Object datepicker, Field field, FontUtilities fontUtilities)
            throws Exception {
        field.setAccessible(true);
        Object yearPicker = field.get(datepicker);
        ((View) yearPicker).setVisibility(View.VISIBLE);

        View childpicker = activity.findViewById(Resources.getSystem().getIdentifier(
                "month", "id", "android"));
        Field field1 = childpicker.getClass().getDeclaredField("mInputText");
        field1.setAccessible(true);
        Object edittext = field1.get(yearPicker);

        Field field2 = childpicker.getClass().getDeclaredField(
                "mSelectorWheelPaint");
        field2.setAccessible(true);
        Object paint = field2.get(yearPicker);
        ((Paint) paint).setTypeface(fontUtilities.scandiaMedium);

        ((TextView) edittext).setTypeface(fontUtilities.scandiaMedium);
        ((TextView) edittext).setLineSpacing(TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP,
                5.0f, Resources.getSystem().getDisplayMetrics()), 1.0f);
    }
}
