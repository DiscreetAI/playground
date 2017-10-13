package data.shark.util;

import android.content.Context;
import android.content.res.AssetManager;
import android.graphics.Typeface;
import android.support.design.widget.TextInputLayout;
import android.widget.TextView;

/**
 * Sets and defines fonts of text throughout the app
 */
public class FontUtilities {
    public Typeface scandiaBold;
    public Typeface scandiaBoldItalic;
    public Typeface scandiaLight;
    public Typeface scandiaLightItalic;
    public Typeface scandiaMedium;
    public Typeface scandiaMediumItalic;
    public Typeface scandiaRegular;
    public Typeface scandiaRegularItalic;
    public Typeface scandiaStencil;
    private AssetManager assets;

    public FontUtilities(Context context) {
        assets = context.getAssets();

        //Instantiate typefaces using context
        scandiaBold = Typeface.createFromAsset(assets, "fonts/Scandia-Bold.otf");
        scandiaBoldItalic = Typeface.createFromAsset(assets, "fonts/Scandia-BoldItalic.otf");
        scandiaLight = Typeface.createFromAsset(assets, "fonts/Scandia-Light.otf");
        scandiaLightItalic = Typeface.createFromAsset(assets, "fonts/Scandia-LightItalic.otf");
        scandiaMedium = Typeface.createFromAsset(assets, "fonts/Scandia-Medium.otf");
        scandiaMediumItalic = Typeface.createFromAsset(assets, "fonts/Scandia-MediumItalic.otf");
        scandiaRegular = Typeface.createFromAsset(assets, "fonts/Scandia-Regular.otf");
        scandiaRegularItalic = Typeface.createFromAsset(assets, "fonts/Scandia-RegularItalic.otf");
        scandiaStencil = Typeface.createFromAsset(assets, "fonts/Scandia-Stencil.otf");
    }

    /**
     * Set the font of a single TextView given a TextView and a Typeface
     */
    public static void setFonts(TextView view, Typeface typeFace) {
        view.setTypeface(typeFace);
    }

    /**
     * Set the fonts of multiple TextViews given an array of TextViews and a Typeface
     */
    public static void setFonts(TextView[] views, Typeface typeface) {
        for (TextView tv : views) {
            tv.setTypeface(typeface);
        }
    }

    /**
     * Set the font of a single TextInputLayout given a TextInputLayout and a Typeface
     */
    public static void setFonts(TextInputLayout layout, Typeface typeface) {
        layout.setTypeface(typeface);
    }

    /**
     * Set the fonts of multiple TextInputLayouts given an array of TextInputLayouts and a Typeface
     */
    public static void setFonts(TextInputLayout[] layouts, Typeface typeface) {
        for (TextInputLayout layout : layouts) {
            layout.setTypeface(typeface);
        }
    }
}
