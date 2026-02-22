package com.example.awrad

import android.content.Context
import android.content.ContextWrapper
import android.os.Build
import android.os.LocaleList
import java.util.Locale

class MyContextWrapper(base: Context) : ContextWrapper(base) {
    companion object {
        fun wrap(context: Context, newLocale: Locale): ContextWrapper {
            var context = context
            val res = context.resources
            val configuration = res.configuration

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
                configuration.setLocale(newLocale)
                val localeList = LocaleList(newLocale)
                LocaleList.setDefault(localeList)
                configuration.setLocales(localeList)
                context = context.createConfigurationContext(configuration)
            } else {
                configuration.setLocale(newLocale)
                context = context.createConfigurationContext(configuration)
            }

            return MyContextWrapper(context)
        }
    }
}
