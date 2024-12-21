const DATA_URL = "https://showcases.yalco.kr/offline/snu-winter-2024/final-project/data.json";

const contents = document.querySelector(".contents");
const main = document.querySelector("main");
const asideUl = document.querySelector("aside ul");

const colors = ["dodgerblue", "darkorange", "mediumseagreen", "mediumpurple", "tomato"];
main.classList.add("dodgerblue");

const colorPicker = document.createElement("div");
colorPicker.classList.add("color-picker");

colors.forEach(color => {
  const colorButton = document.createElement("button");
  colorButton.classList.add(color);
  colorButton.classList.add("color-button");
  colorPicker.appendChild(colorButton);
  colorButton.addEventListener("click", () => {
    colors.forEach(c => main.classList.remove(c));
    main.classList.add(color);
  });
});

main.appendChild(colorPicker);
asideUl.classList.add("js-react-switch");

async function loadData() {
  const response = await fetch(DATA_URL);
  const data = await response.json();
  console.log(data);

  data.forEach(item => {

    const li = document.createElement("li");
    li.classList.add(item.id);
    li.textContent = item.name;
    li.addEventListener("click", () => {
      contents.classList.remove("js", "react");
      contents.classList.add(item.id);
    });
    asideUl.appendChild(li);

    const section = document.createElement("section");
    section.classList.add("js-react");
    section.classList.add(item.id);

    const nameElement = document.createElement("h1");
    nameElement.textContent = item.name;
    section.appendChild(nameElement);

    const definitionElement = document.createElement("p");
    definitionElement.textContent = item.definition;
    section.appendChild(definitionElement);

    const tagsList = document.createElement("ul");
    tagsList.classList.add("tags");
    item.tags.forEach(feature => {
      const featureItem = document.createElement("li");
      featureItem.textContent = '#' + feature;
      tagsList.appendChild(featureItem);
    });
    section.appendChild(tagsList);

    const characteristicsTitle = document.createElement("h2");
    characteristicsTitle.textContent = "주요 특징";
    section.appendChild(characteristicsTitle);

    const characteristicsList = document.createElement("ul");
    characteristicsList.classList.add("characteristics");

    item.keyCharacteristics.forEach(characteristic => {
      const characteristicItem = document.createElement("li");

      const subtitle = document.createElement("strong");
      subtitle.textContent = characteristic.subtitle;
      characteristicItem.appendChild(subtitle);

      characteristicItem.appendChild(document.createElement("br"));

      const description = document.createElement("span");
      description.textContent = characteristic.description;
      characteristicItem.appendChild(description);

      characteristicsList.appendChild(characteristicItem);
    });
    section.appendChild(characteristicsList);

    main.appendChild(section);
  });

  contents.classList.add(data[0].id);
}

loadData();