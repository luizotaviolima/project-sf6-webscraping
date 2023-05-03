from functions import site_content, site_target_content, get_web_info, get_character_link, \
    char_detail_text, dataframe, export_to_csv, work_directory, clean_directory
from datetime import datetime
import os


if __name__ == "__main__":

    # Setting path to save csv files
    dataPath = work_directory()
    os.chdir(dataPath)

    # Variables
    url = 'https://www.streetfighter.com/6/pt-br/character/'
    tagsList = ['div', 'a', 'p', 'ul', 'span']
    attributes = {'attr01': {'class': 'character__select__list'},
                  'attr02': {'class': 'character__detail__profile__text'},
                  'attr03': {'class': 'character__detail__profile__info'},
                  'attr04': {'class': 'info__item__text'}}
    detailColumns = [
        'nome', 'descricao', 'odeia', 'curte', 'altura', 'peso', 'timestamp']

    FullContent = site_content(url=url)

    TargetContent = site_target_content(
        site_full_content=FullContent, tag=tagsList, attrs=attributes.get('attr01'))

    htmlCharNameAndLink = get_web_info(
        site_target_content=TargetContent, tag=tagsList[1])

    characterLinkList = get_character_link(html_content=htmlCharNameAndLink)

    # Clean destiny folder before saving files
    clean_directory(work_directory=dataPath)

    # Extraction all character information

    for characterLink in characterLinkList:
        # Getting character name from list above
        charName = characterLink.split("/")[4].split(".")[0].capitalize()
        print(f"Getting {charName} information")

        # Character link and full site content
        charUrl = 'https://www.streetfighter.com' + characterLink
        charFullContent = site_content(url=charUrl)

        # Getting character description
        charDescription = site_target_content(
            site_full_content=charFullContent, tag=tagsList[2], attrs=attributes.get('attr02'))
        charFullInfo = [charName, charDescription.text]

        # Getting character detail
        charDetail = site_target_content(
            site_full_content=charFullContent, tag=tagsList[3], attrs=attributes.get('attr03'))

        charDetailText = char_detail_text(
            char_detail=charDetail, tag=tagsList[4], attrs=attributes.get('attr04'))

        for text in charDetailText:
            charFullInfo.append(text.text)

        # Appending timestamp info
        charFullInfo.append(datetime.now())

        # Creating a DataFrame
        dfCharInfo = dataframe(char_full_info=charFullInfo,
                               columns_name=detailColumns)

        # Exporting to csv
        export_to_csv(dfCharInfo, charName)
