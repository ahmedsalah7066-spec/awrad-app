package com.example.awrad.di

import com.example.awrad.data.repository.SettingsRepositoryImpl
import com.example.awrad.data.repository.SimpleContentRepository
import com.example.awrad.domain.repository.SettingsRepository
import com.example.awrad.domain.repository.WirdRepository
import dagger.Binds
import dagger.Module
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    @Singleton
    abstract fun bindSettingsRepository(
        impl: SettingsRepositoryImpl
    ): SettingsRepository

    @Binds
    @Singleton
    abstract fun bindWirdRepository(
        impl: SimpleContentRepository
    ): WirdRepository
}
