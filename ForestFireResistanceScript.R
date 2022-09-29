library(tidyverse) # carrega o pacote tidyverse

ForestFire <- read.csv(file = 'output/ForestFireResistance_model_data _iter_ 100 _steps_ 100 _ 2022-09-15 -18:12:03.601742.csv') #Leitura do arquivo CSV

ForestFire <- ForestFire[ForestFire$density > 0,] #remove do dataset linhas de simulações sem agentes

ForestFire <- select(ForestFire, -c(width, height)) #remove do dataset colunas não úteis para a análise

ggplot(data = ForestFire, mapping = aes(group = density, y = Escaped.Tax)) + geom_boxplot() #Cria o primeira figura com boxplot, que mostra a taxa de árvores que escaparam (Escaped Tax) com a densidade (density) como grupo.

ggplot(data = ForestFire, mapping = aes(group = intensity, y = Escaped.Tax)) + geom_boxplot() #Cria a segunda figura com boxplot, que mostra a taxa de árvores que escaparam (Escaped Tax) com a intensidade do fogo (intensity) como grupo.

ggplot(data = ForestFire, mapping = aes(x = Step, colour = Escaped.Tax)) + geom_freqpoly(binwidth = 0.01) #Cria a figura com um histograma, mostrando a taxa de árvores escapando (Escaped Tax) relacionando-as com as etapas (Step).


