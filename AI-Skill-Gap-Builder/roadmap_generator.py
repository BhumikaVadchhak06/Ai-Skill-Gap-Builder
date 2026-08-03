def generate_roadmap(missing_skills):

    roadmap = []

    week = 1

    for skill in missing_skills:

        roadmap.append(
            f"Week {week}: Learn {skill}"
        )

        week += 1

    return roadmap