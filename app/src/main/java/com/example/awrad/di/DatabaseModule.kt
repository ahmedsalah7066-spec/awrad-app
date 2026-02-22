package com.example.awrad.di

import android.content.Context
import androidx.room.Room
import com.example.awrad.data.room.AppDatabase
import com.example.awrad.data.room.TranslationDao
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideAppDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "awrad_database"
        )
        .fallbackToDestructiveMigration()
        .build()
    }

    @Provides
    fun provideTranslationDao(database: AppDatabase): TranslationDao {
        return database.translationDao()
    }
}
